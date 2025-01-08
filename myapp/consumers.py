from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import pandas as pd
import plotly.express as px

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

        # Send initial plot data to the WebSocket when it connects
        await self.send_plot_data()

    async def disconnect(self, close_code):
        # Optionally handle the disconnection
        pass

    async def receive(self, text_data):
        # Handle incoming data from the WebSocket (if necessary)
        pass

    @sync_to_async
    def get_customer_data(self):
        # This function interacts with the database and is synchronous,
        # so we use `sync_to_async` to call it inside an async function.
        from .models import CustomerData
        return list(CustomerData.objects.all().values())

    async def send_plot_data(self):
    # Get customer data
        queryset = await self.get_customer_data()
        df = pd.DataFrame(queryset)
        df['marital_status'] = df['marital_status'].replace({0: 'Married', 1: 'Single'})
        # Gender by Total Amount
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
        # Gender Count
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

    
        df['age_group'] = df['age_group'].astype('category')
        df_grouped_gender = df.groupby('age_group', as_index=False)['amount'].sum()
        fig_gender_pie = px.pie(df_grouped_gender,names="age_group",
                        values="amount", 
                        title="Total Amount With Age Group", 
                        labels={"age_group": "Age Group", "amount": "Total Amount"},
                        hole=0.4,
                        ) # Custom colors
        fig_gender_pie.update_layout(
            width=400,  # Width of the graph
            height=400,  # Height of the graph
            margin=dict(l=20, r=20, t=30, b=20),  # Adjust margins for better fitting
            font=dict(family="Arial, sans-serif", size=12),  # Change font family and size
        )
        # Display the plot in HTML format
     
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
        status_counts = df['marital_status'].value_counts().reset_index()
        status_counts.columns = ['Marital Status', 'Count']

        # Create a Plotly bar chart
        fig_martial = px.bar(
            status_counts,
            x="Marital Status",
            y="Count",
            color="Marital Status",
            title="Count of Single and Married Individuals",
            labels={"Count": "Number of People", "Marital Status": "Marital Status"},
        )

        # Customize layout
        fig_martial.update_layout(
            width=400,  # Chart width
            height=400,  # Chart height
            margin=dict(l=20, r=20, t=30, b=20),  # Margins for better fitting
            font=dict(family="Arial, sans-serif", size=12),  # Font styling
        )

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

         
        df_product_category = df.groupby('product_category', as_index=False)['amount'].sum()
        product_category=px.treemap(df_product_category,path=["product_category"],values="amount",title="Sales Amount Of Product Category")
        product_category.update_layout(
            width=400,  # Chart width
            height=400,  # Chart height
            margin=dict(l=20, r=20, t=30, b=20),  # Margins for better fitting
            font=dict(family="Arial, sans-serif", size=12),  # Font styling
        )
         
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

        # Send plot data as JSON
        await self.send(text_data=json.dumps({
            'plot_gender': fig_gender.to_json(),
            'plot_count': fig_count.to_json(),
            "slack_bars":fig.to_json(),
            'pi_graph':fig_gender_pie.to_json(),
            'fig_state':fig_state.to_json(),
            'fig_state_amount':fig_state_amount.to_json(),
            'fig_martial':fig_martial.to_json(),
            'df_gender_martial_status':fig_gender_martial_status.to_json(),
            'fig_count_df_occupation':fig_count_df_occupation.to_json(),
            'fig_occupation_by_amount':fig_occupation_by_amount.to_json(),
            'fig_product_category':fig_product_category.to_json(),
            'product_category':product_category.to_json(),
            'fig_product_id': fig_product_id.to_json()
        }))
        

# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # This method is called when the WebSocket is handshaking as part of the connection process
#         self.room_name = 'chat_room'  # Use a room name for the chat
#         self.room_group_name = f'chat_{self.room_name}'

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # This method is called when the WebSocket closes
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         # This method is called when we receive a message from WebSocket
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Create a new group for the WebSocket connection
        self.room_name = 'chat_group'
        self.room_group_name = f'chat_group'

        # Join the WebSocket group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        username = text_data_json['username']
        content = text_data_json['content']

        # Get the current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Send the message to the WebSocket group with the timestamp
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'username': username,
                'content': content,
                'timestamp': timestamp
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'username': event['username'],
            'content': event['content'],
            'timestamp': event['timestamp']
        }))
