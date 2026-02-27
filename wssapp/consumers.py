from channels.generic.websocket import AsyncWebsocketConsumer
import json
from products.models import Product, StockMovement
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = 'stock_updates'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("Disconnected")

    async def receive(self, text_data=None):
        # এই মেথডটি এখন ম্যানুয়ালি লেটেস্ট ডাটা রিফ্রেশ করতে ব্যবহার করা যেতে পারে
        stock_movement = await StockMovement.objects.filter(
            created_at__date=timezone.now().date()
        ).select_related('product').order_by('-created_at').afirst()
        
        if stock_movement:
            await self.send(text_data=json.dumps({
                'type': 'stock_update',
                'stock_movements': stock_movement.new_stock,
                'product_name': stock_movement.product.name,
                'movement_type': stock_movement.get_movement_type_display(),
                'quantity': stock_movement.quantity,
            }))

    async def stock_update(self, event):
        # Signal থেকে আসা ডাটা ক্লায়েন্টে পাঠানো
        await self.send(text_data=json.dumps(event))