{
    "name": "Mini Ecommerce",
    "version": "1.0",
    "depends": ["base", "web"],
    "author": "Your Name",
    "category": "Sales",
    "description": """
    Mini Ecommerce System
    """,
    "data": [
        "security/ir.model.access.csv",
        "views/customer_view.xml",
        "views/category_view.xml",
        "views/product_view.xml",
        "views/order_view.xml",
        "views/menu.xml",
    ],
    "installable": True,
    "application": True,
}
