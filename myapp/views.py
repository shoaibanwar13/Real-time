# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from nltk.corpus import wordnet
# from textblob import TextBlob
# import random
# import re
# from .serializers import TextRequestSerializer

# # Ensure NLTK resources are downloaded
# import nltk
# nltk.download('wordnet')
# nltk.download('punkt')

# class UnpredictableTextGenerator:
#     def __init__(self, text, order=3):
#         self.order = order
#         self.chain = {}
#         self.words = self.tokenize(text)
#         self.add_to_chain()

#     def tokenize(self, text):
#         return re.findall(r'\b\w+\b|[.,!?]', text)

#     def add_to_chain(self):
#         for i in range(len(self.words) - self.order):
#             current_tuple = tuple(self.words[i:i + self.order])
#             next_word = self.words[i + self.order]
#             if current_tuple in self.chain:
#                 if next_word not in self.chain[current_tuple]:
#                     self.chain[current_tuple].append(next_word)
#             else:
#                 self.chain[current_tuple] = [next_word]

#     def generate_text(self, input_length):
#         required_length = max(1, int(input_length * 1.2))
#         start_tuple = random.choice(list(self.chain.keys()))
#         sentence = list(start_tuple)

#         while len(sentence) < required_length:
#             current_tuple = tuple(sentence[-self.order:])
#             next_words = self.chain.get(current_tuple, None)
#             if not next_words:
#                 break
#             next_word = random.choice(next_words)
#             sentence.append(next_word)

#         if sentence:
#             sentence[0] = sentence[0].capitalize()

#         output_sentence = ' '.join(sentence)
#         output_sentence = re.sub(r'\s+[.,!?]', lambda match: match.group(0).strip(), output_sentence)
#         output_sentence = re.sub(r'([.!?]){2,}', r'\1', output_sentence)

#         if output_sentence and output_sentence[-1] not in ['.', '!', '?']:
#             output_sentence += '.'

#         output_sentence = self.replace_with_synonyms(output_sentence)
#         output_sentence = self.correct_grammar(output_sentence)

#         return output_sentence

#     def replace_with_synonyms(self, sentence):
#         words = sentence.split()
#         new_words = []
#         for word in words:
#             if word.lower() in ['the', 'and', 'of', 'to', 'in', 'a', 'an']:
#                 new_words.append(word)
#                 continue

#             synonyms = wordnet.synsets(word)
#             if synonyms:
#                 synonym = random.choice(synonyms).lemmas()[0].name()
#                 if synonym != word:
#                     new_words.append(synonym.replace('_', ' '))
#                 else:
#                     new_words.append(word)
#             else:
#                 new_words.append(word)
#         return ' '.join(new_words)

#     def correct_grammar(self, sentence):
#         blob = TextBlob(sentence)
#         return str(blob.correct())

# class GenerateTextView(APIView):
#     def post(self, request):
#         serializer = TextRequestSerializer(data=request.data)
#         if serializer.is_valid():
#             text = serializer.validated_data['text']
#             input_length = len(text.split())
#             generator = UnpredictableTextGenerator(text)
#             generated_text = generator.generate_text(input_length)
#             return Response({"language": serializer.validated_data['language'], "generated_text": generated_text}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import pandas as pd
import plotly.express as px
from django.shortcuts import render
from .models import CustomerData
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import logging

# Set up logging
logger = logging.getLogger(__name__)
CACHE_TTL = getattr(settings ,'CACHE_TTL' , DEFAULT_TIMEOUT)

# View to generate the bar plots and display them in the dashboard
def dashboard_view(request):
    # Fetch all CustomerData from the database
    cache_key = 'customer_data'  # Unique key for the cached data
    queryset = cache.get(cache_key)  # Try to fetch data from the cache

    if queryset is None:
        queryset = CustomerData.objects.all()  # Fetch from the database
        print("Data Coming From DB")
        logger.info("Data fetched from the database.")
        print("Data fetched from the database.")  # Debug message for testing
        cache.set(cache_key, queryset, timeout=3600)  # Store in cache for 1 hour
    else:
        logger.info("Data fetched from the cache.")
        print("Data fetched from the cache.")  # Debug message for testing
    # Convert the queryset into a pandas DataFrame
    df = pd.DataFrame(list(queryset.values()))
    df['marital_status'] = df['marital_status'].replace({0: 'Married', 1: 'Single'})
     
     

    # Ensure 'gender' is treated as a categorical variable
    

    # First chart: Gender by Total Amount
    df_grouped_gender = df.groupby('gender', as_index=False)['amount'].sum()
    fig_gender = px.bar(df_grouped_gender, x="gender", y="amount", 
                        title="Total Amount by Gender", 
                        labels={"gender": "Gender", "Amount": "Total Amount"},
                        color="gender",
                        
                        )  # Custom colors
    fig_gender.update_layout(
        width=400,  # Width of the graph
        height=400,  # Height of the graph
        margin=dict(l=20, r=20, t=30, b=20),  # Adjust margins for better fitting
        font=dict(family="Arial, sans-serif", size=12),  # Change font family and size
    )
    plot_html_gender = fig_gender.to_html(full_html=False)

    # Second chart: Gender by Count (example: count of entries per gender)
    df_gender_count = df['gender'].value_counts().reset_index()
    df_gender_count.columns = ['gender', 'count']
    fig_count = px.bar(df_gender_count, x="gender", y="count", 
                       title="Gender Count", 
                       labels={"gender": "Gender", "count": "Count"},
                       color="gender")  # Custom colors
    fig_count.update_layout(
        width=400,  # Width of the graph
        height=400,  # Height of the graph
        margin=dict(l=20, r=20, t=30, b=20),  # Adjust margins
        font=dict(family="Arial, sans-serif", size=12),  # Font styling
    )
   
    plot_html_count = fig_count.to_html(full_html=False)
    df['age_group'] = df['age_group'].astype('category')
    df_grouped_gender = df.groupby('age_group', as_index=False)['amount'].sum()
    fig_gender = px.pie(df_grouped_gender,names="age_group",
                    values="amount", 
                    title="Total Amount With Age Group", 
                    labels={"age_group": "Age Group", "amount": "Total Amount"},
                    hole=0.6,
                    ) # Custom colors
    fig_gender.update_layout(
        width=400,  # Width of the graph
        height=400,  # Height of the graph
        margin=dict(l=20, r=20, t=30, b=20),  # Adjust margins for better fitting
        font=dict(family="Arial, sans-serif", size=12),  # Change font family and size
    )
    plot_html_age_group = fig_gender.to_html(full_html=False)

    # Assuming 'df' has 'gender', 'age_group', and 'amount' columns
    # If there's no 'age_group' column, you may need to create one (you can bin age into groups)

    # Group the data by age_group and gender and sum the amounts
    df_grouped = df.groupby(['age_group', 'gender'], as_index=False)['amount'].sum()

    # Create a stacked bar chart with Plotly
    fig = px.bar(df_grouped, 
                x="age_group", 
                y="amount", 
                color="gender",  # Split the bars by Gender (M and F)
                title="Total Amount by Gender and Age Group", 
                labels={"age_group": "Age Group", "amount": "Total Amount", "gender": "Gender"}, 
                barmode="stack")  # Stack the bars for gender split

    # Add data labels inside the bars
    fig.update_traces(texttemplate='%{text}', textposition='inside', 
                    text=df_grouped['amount'])

    # Update the layout for better display
    fig.update_layout(
        width=400,  # Width of the graph
        height=400,  # Height of the graph
        margin=dict(l=20, r=20, t=30, b=20),  # Adjust margins for better fitting
        font=dict(family="Arial, sans-serif", size=12),  # Change font family and size
    )

    # Display the plot in HTML format
    plot_html_count_age_by = fig.to_html(full_html=False)
    orders_from_state = df.groupby('state', as_index=False)['orders'].sum()
    fig_state = px.bar(orders_from_state, x="state", y="orders", 
                        title="Orders From All States", 
                        labels={"state": "State", " orders": "Orders"},
                        color="state")  # Custom colors
    fig_state.update_layout(
        width=400,  # Width of the graph
        height=400,  # Height of the graph
        margin=dict(l=20, r=20, t=30, b=20),  # Adjust margins for better fitting
        font=dict(family="Arial, sans-serif", size=12),  # Change font family and size
    )
    plot_html_states = fig_state.to_html(full_html=False)
    
    total_amount_from_state = df.groupby('state', as_index=False)['amount'].sum()
    fig_state_amount = px.bar(total_amount_from_state, x="state", y="amount", 
                        title="Orders From All States", 
                        labels={"state": "State", "amount": "Amount"},
                        color="state")  # Custom colors
    fig_state_amount.update_layout(
        width=400,  # Width of the graph
        height=400,  # Height of the graph
        margin=dict(l=20, r=20, t=30, b=20),  # Adjust margins for better fitting
        font=dict(family="Arial, sans-serif", size=12),  # Change font family and size
    )
    plot_html_states_amount = fig_state_amount.to_html(full_html=False)
    status_counts = df['marital_status'].value_counts().reset_index()
    status_counts.columns = ['Marital Status', 'Count']

    # Create a Plotly bar chart
    fig = px.bar(
        status_counts,
        x="Marital Status",
        y="Count",
        color="Marital Status",
        title="Count of Single and Married Individuals",
        labels={"Count": "Number of People", "Marital Status": "Marital Status"},
    )

    # Customize layout
    fig.update_layout(
        width=400,  # Chart width
        height=400,  # Chart height
        margin=dict(l=20, r=20, t=30, b=20),  # Margins for better fitting
        font=dict(family="Arial, sans-serif", size=12),  # Font styling
    )

    # Convert the chart to HTML
    plot_html = fig.to_html(full_html=False)
    df_gender_martial_status = (
    df.groupby(['marital_status', 'gender'], as_index=False)['amount']
    .sum()
    .sort_values(by="amount", ascending=True)
)

    # Create a bar chart using Plotly
    fig_gender_martial_status = px.bar(
        df_gender_martial_status,
        x="marital_status",
        y="amount",
        color="gender",
        title="Total Amount by Gender and Marital Status",
        labels={"amount": "Total Amount", "marital_status": "Marital Status", "gender": "Gender"},
    )

    # Customize layout
    fig_gender_martial_status.update_layout(
        width=400,  # Width of the graph
        height=400,  # Height of the graph
        margin=dict(l=20, r=20, t=30, b=20),  # Adjust margins for better fitting
        font=dict(family="Arial, sans-serif", size=12),  # Font styling
    )

    # Convert the chart to HTML
    plot_html_fig_gender_martial_status = fig_gender_martial_status.to_html(full_html=False)
    df_occupation = df['occupation'].value_counts().reset_index()
    df_gender_count.columns = ['occupation', 'count']
    fig_count_df_occupation = px.pie(df_occupation,names="occupation", 
                       values="count",
                       title="Occupation Count", 
                       labels={"occupation": "Occupation", "count": "Count"},
                       color="occupation",
                       )  # Custom colors
    fig_count_df_occupation .update_layout(
        width=400,  # Width of the graph
        height=400,  # Height of the graph
        margin=dict(l=20, r=20, t=30, b=20),  # Adjust margins
        font=dict(family="Arial, sans-serif", size=12),  # Font styling
    )
   
    plot_html_count_occupation = fig_count_df_occupation .to_html(full_html=False)
    df_occupation_by_amount = df.groupby('occupation', as_index=False)['amount'].sum()
    fig_occupation_by_amount = px.pie(df_occupation_by_amount,names="occupation",
                    values="amount", 
                    title="Total Amount With Customers Occupations", 
                    labels={"occupation": "Occupation", "amount": "Total Amount"},
                    hole=0.3,
                    ) # Custom colors
    fig_occupation_by_amount.update_layout(
        width=400,  # Width of the graph
        height=400,  # Height of the graph
        margin=dict(l=20, r=20, t=30, b=20),  # Adjust margins for better fitting
        font=dict(family="Arial, sans-serif", size=12),  # Change font family and size
    )
    plot_html_fig_occupation_by_amount = fig_occupation_by_amount.to_html(full_html=False)
    product_category_counts = df['product_category'].value_counts().reset_index()
    product_category_counts.columns = ['product_category', 'Count']

    # Create a Plotly bar chart
    fig_product_category = px.bar(
        product_category_counts,
        x="product_category",
        y="Count",
        color="product_category",
        title="Count of Product Category",
        labels={"Count": "Product Category  Count", "product_category": "Product Category"},
    )

    # Customize layout
    fig_product_category.update_layout(
        width=400,  # Chart width
        height=400,  # Chart height
        margin=dict(l=20, r=20, t=30, b=20),  # Margins for better fitting
        font=dict(family="Arial, sans-serif", size=12),  # Font styling
    )

    # Convert the chart to HTML
    plot_html_product_category = fig_product_category.to_html(full_html=False)
    df_product_category = df.groupby('product_category', as_index=False)['amount'].sum()
    product_category=px.treemap(df_product_category,path=["product_category"],values="amount",title="Sales Amount Of Product Category")
    product_category.update_layout(
        width=400,  # Chart width
        height=400,  # Chart height
        margin=dict(l=20, r=20, t=30, b=20),  # Margins for better fitting
        font=dict(family="Arial, sans-serif", size=12),  # Font styling
    )
    df_product_category=product_category.to_html(full_html=False)
    top_ten_sold_product=df.groupby(["product_id","product_category"],as_index=False)["orders"].sum().sort_values(by='orders', ascending=False).head(10)

    fig_product_id=px.sunburst(top_ten_sold_product,path=["product_id","product_category"],values="orders",
                              title='Orders by Product ID ',
                              labels={'x': 'Product ID', 'y': 'Order Count'})
    fig_product_id.update_layout(
        width=400,  # Chart width
        height=400,  # Chart height
        margin=dict(l=20, r=20, t=30, b=20),  # Margins for better fitting
        font=dict(family="Arial, sans-serif", size=12),  # Font styling
    )
    html_fig_product=fig_product_id.to_html(full_html=False)
    # Pass both plot HTMLs to the template
    return render(request, 'dashboard.html', {'plot_html_gender': plot_html_gender, 'plot_html_count': plot_html_count,"plot_html_age_group":plot_html_age_group,"plot_html_count_age_by":plot_html_count_age_by,"plot_html_states":plot_html_states,"plot_html_states_amount":plot_html_states_amount,"plot_html":plot_html,"plot_html_fig_gender_martial_status":plot_html_fig_gender_martial_status,"plot_html_count_occupation":plot_html_count_occupation,"plot_html_fig_occupation_by_amount":plot_html_fig_occupation_by_amount,"plot_html_product_category":plot_html_product_category,"df_product_category":df_product_category,"html_fig_product":html_fig_product})
# # views.py
# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import CustomerData

# def insert_customer_data():
#     # You can replace these values with the actual data you want to insert
#     row = {
#         'User_ID': 657890876543,
#         'Cust_name': 'John Doe',
#         'Product_ID': 1239900977,
#         'Gender': 'Male',
#         'Age Group': '25-34',
#         'Age': 30,
#         'Marital_Status': 1,
#         'State': 'California',
#         'Zone': 'West',
#         'Occupation': 'Engineer',
#         'Product_Category': 'Electronics',
#         'Orders': 5,
#         'Amount': 500.0
#     }

#     # Insert data into the CustomerData model
#     customer_data = CustomerData.objects.create(
#         user_id=row['User_ID'],
#         cust_name=row['Cust_name'],
#         product_id=row['Product_ID'],
#         gender=row['Gender'],
#         age_group=row["Age Group"],
#         age=row["Age"],
#         marital_status=row["Marital_Status"],
#         state=row["State"],
#         zone=row["Zone"],
#         occupation=row["Occupation"],
#         product_category=row["Product_Category"],
#         orders=row["Orders"],
#         amount=row["Amount"]
#     )
    
#     # Return the inserted customer's ID as confirmation
#     return customer_data.id

# def insert_data_view():
#     # Call the function to insert data
#     customer_id = insert_customer_data()

#     # Return a response with the inserted customer's ID
#     return JsonResponse({
#         'status': 'success',
#         'message': f'Customer data inserted successfully with ID {customer_id}'
#     })
# insert_data_view()


# project_management/views.py
# from rest_framework import viewsets
# from .models import Sprint, UserStory, Task,KanbanBoard, KanbanColumn, KanbanCard
# # from .serilizers import SprintSerializer, UserStorySerializer, TaskSerializer,KanbanBoardSerializer, KanbanColumnSerializer, KanbanCardSerializer
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from rest_framework.response import Response
# from django.shortcuts import render, get_object_or_404, redirect 

# class SprintViewSet(viewsets.ModelViewSet):
#     queryset = Sprint.objects.all()
#     serializer_class = SprintSerializer

# class UserStoryViewSet(viewsets.ModelViewSet):
#     queryset = UserStory.objects.all()
#     serializer_class = UserStorySerializer

# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer


# class KanbanBoardViewSet(viewsets.ModelViewSet):
#     queryset = KanbanBoard.objects.all()
#     serializer_class = KanbanBoardSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

# class KanbanColumnViewSet(viewsets.ModelViewSet):
#     queryset = KanbanColumn.objects.all()
#     serializer_class = KanbanColumnSerializer
#     permission_classes = [IsAuthenticated]

# class KanbanCardViewSet(viewsets.ModelViewSet):
#     queryset = KanbanCard.objects.all()
#     serializer_class = KanbanCardSerializer
#     permission_classes = [IsAuthenticated]
#     def perform_create(self, serializer):
#         column = KanbanColumn.objects.get(id=serializer.validated_data['column'].id)
#         current_cards_count = column.cards.count()

#         if column.wip_limit > 0 and current_cards_count >= column.wip_limit:
#             return Response(
#                 {"detail": "WIP limit exceeded."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         serializer.save()


from django.http import JsonResponse
from .models import Message

def home(request):
     
    return render(request, 'base.html')

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from .models import Message

def send_chat_message(request):
    if request.method == 'POST':
        username = request.POST['username']
        content = request.POST['content']
        message = Message.objects.create(username=username, content=content)

        # Broadcast the message to WebSocket clients
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'chat_group',  # The WebSocket group name
            {
                'type': 'chat_message',
                'message': content,
                'username': username
            }
        )

        return JsonResponse({
            'username': message.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
# import redis

# # Replace with your actual Redis URL
# REDIS_URL = "rediss://red-ctufmpl2ng1s739dlicg:YGPl2OKvn8JVpUa0O4ZEU3lHyKIUAVaN@singapore-redis.render.com:6379"

# try:
#     # Connect to Redis using the URL
#     redis_client = redis.from_url(REDIS_URL, decode_responses=True)

#     # Test the connection
#     redis_client.ping()
#     print("Redis connection successful!")
# except redis.AuthenticationError:
#     print("Authentication failed! Check your Redis credentials.")
# except Exception as e:
#     print(f"Error connecting to Redis: {e}")
