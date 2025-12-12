from django.db import models

from django.contrib.auth.models import User

from datetime import timedelta


CATEGORY_CHOICES = (
    ('PIANO','Piano'),
    ('E_GUITER','E_Guiter'),
    ('A_Guiter','A_Guiter'),
    ('KEY_BOARD','Key_Board'),
    ('FLUTE','FLUTE'),
    ('VIOLIN','Violin'),
    ('DRUMS','Drums'),
    ('TRUMPETS','TRUMPETS'),
    ('PADS','Pads'),
    ('SAXOPHONE','Saxophone'),
    ('SITAR','Sitar')
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=20)
    product_image = models.ImageField(upload_to='product')
    def __str__(self):
            return f"{self.title} - {self.brand} ({self.category})"
    

ADDRESS_CHOICES = {
     ('HOME','Home'),
     ('WORK','Work')
}
    
class Coustomer_Details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length= 50)
    mobile = models.CharField(max_length=15)
    category = models.CharField(choices=ADDRESS_CHOICES,max_length=20)
    address = models.CharField(max_length=60)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)    
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')
    def __str__(self):
        return f"Name: {self.name} \n Mobile Number: {self.mobile}\n Category: {self.category}\n Address: {self.address},{self.city},{self.pincode},{self.state},{self.country}"
    
class Cart(models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE)
     product = models.ForeignKey(Product,on_delete=models.CASCADE)
     quantity = models.PositiveIntegerField(default=1)

     @property
     def total_cost(self):
          return self.quantity * self.product.discount_price
     

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Packed', 'Packed'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Cancled','Cancled')
]

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Coustomer_Details, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default=None, null=True, blank=True)

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price+500
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"
    

class Order_Placed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_address = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default=None, null=True, blank=True)


    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price+500
    
    @property
    def delivered_on(self):
        return self.ordered_date + timedelta(days=7)
    




class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " - " + self.subject

    

    
    
    
     