# virtual_sales_agent.py

import csv
from transformers import pipeline

class VirtualSalesAgent:
    def __init__(self, contact_file):
        self.contacts = self.load_contacts(contact_file)
        self.sales_pipeline = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

    def load_contacts(self, contact_file):
        contacts = []
        with open(contact_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                contacts.append(row)
        return contacts

    def make_sales_call(self, prospect):
        sales_pitch = self.sales_pipeline(
            f"Hello {prospect['Name']}, this is [Your Name] from [Your Company]. I noticed that {prospect['Company']} is in the market for a new {prospect['Product']}. Our {prospect['Product']} offers {prospect['Benefits']}. Would you be interested in learning more?"
        )
        return sales_pitch[0]['generated_text']

    def close_deal(self, objection_handling):
        response = self.sales_pipeline(objection_handling)
        return response[0]['generated_text']

def main():
    contact_file = "contacts.csv"
    sales_agent = VirtualSalesAgent(contact_file)

    # Make sales calls to each contact
    for contact in sales_agent.contacts:
        sales_pitch = sales_agent.make_sales_call(contact)
        print(f"\nSales Pitch for {contact['Name']} at {contact['Company']}:")
        print(sales_pitch)

    # Handle objections and close the deal
    objection_handling = "I'm not sure if we have the budget for this."
    response = sales_agent.close_deal(objection_handling)
    print("\nResponse to Objection:")
    print(response)

if __name__ == "__main__":
    main()
    
