# AQUA MANAGER APP

## Problem Statement
Aqua manager aims to revolutionize the pure water supply chain in Nigeria by developing a comprehensive app ecosystem, addressing the longstanding issues of accessibility, transparency, and financial efficiency. 
The challenge is to seamlessly connect individuals, supermarkets, and depots through a unified platform, ensuring reliable water delivery while navigating the complexities of the Nigerian logistics landscape. 
While Aqua Manager strives to optimize the end-to-end supply chain, it acknowledges the external factors that might pose challenges, emphasizing the need for adaptability and resilience in the face of ever-changing circumstances. 
The challenge is not just to create a technological solution but to forge a reliable and efficient network that can withstand the unique challenges of the Nigerian market and contribute to the accessibility and transparency of pure water distribution.

## Where to find the app online
- Coming Soon !!!

## How to run the app locally using vscode
- Clone the app
- Ensure Python and Flask and sql-connector-python are installed on your VSCODE
- Install and setup your MySql Server
    - Create a database called requests
    - Install MySQL extension on VSCODE
- Install flash to manage the flash messages if need be.
- Run the app (run python app.py via terminal)

## MVP User Stories
- Customer
    - As a customer, I want to be able to request for water to be delivered to my location.
    - I should be able to see my delivery status.
- Factory Worker
    - As a factory worker, I should be able to view and edit customer request and update request status when the water has been delivered.
    - I should be able to add/edit packs/bags of water produced.
- Factory Owner / Manager
    - As a manager, I should have a dashboard that gives the reuests summary for the day.
    - I should be able to have a summarized view of production data for the day.
    - I should be able to view all outstanding requests that are yet to be actioned upon.

## Expanded User Stories
- For the app
    - Have a mobile app.
    - Ability to onboard different water company with their own different admin and dashboard pages.
    - Login functionalities for customers and companies. Customers should be able to proceed as guest if they wish.
    - Integrate using Google location apis for customer view.
    - Integrate payment gateway for transactions.

- Customer
    - Have the ability to login and manage my profile or choose to use the app as a guest
    - Have the ability to select the water company in my vicinity that should deliver to me.
    - Have the ability to complete payment on portal or pay on delivery.

- Water Company
    - Have a master page for company and ensure the company is the verified company.
    - Login capabilities is a must have.
    - Have the ability to manage accesses for factory workers.
    - Have the ability to manage cost price for the products.
    - Have a cost analysis and reporting template for water produced and sold.
    - Expenses management.

&copy; Copyright 2024 by lagra-iku & Olisajioke


