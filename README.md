# AQUA MANAGER APP

## Introduction
Aqua manager aims to revolutionize the pure water supply chain in Nigeria by developing a comprehensive app ecosystem, addressing the longstanding issues of accessibility, transparency, and financial efficiency. 
The challenge is to seamlessly connect individuals, supermarkets, and depots through a unified platform, ensuring reliable water delivery while navigating the complexities of the Nigerian logistics landscape. 
While Aqua Manager strives to optimize the end-to-end supply chain, it acknowledges the external factors that might pose challenges, emphasizing the need for adaptability and resilience in the face of ever-changing circumstances. 
The challenge is not just to create a technological solution but to forge a reliable and efficient network that can withstand the unique challenges of the Nigerian market and contribute to the accessibility and transparency of pure water distribution.

## Architecture of the app
![Architecture of Aqua manager](URL "https:\\app.aquamanager.com.ng\static\images\aqua_manager_architecture.png")

## Where to find the app online?
- [Landing Page](https:\\aquamanager.com.ng)
- [App Page](https:\\app.aquamanager.com.ng)

## Authors
- [Grace O. Nweke](https://github.com/lagra-iku)
- [Olisajiokem Ahunanya](https://github.com/Olisajioke)

## Usage
To be used by pure water manufacturing companies in Naija.

## How to run the app locally using vscode?
- Clone the app
- Ensure Python and Flask and sql-connector-python are installed on your VSCODE
- Install and setup your MySql Server
    - Create a database called requests
    - Install MySQL extension on VSCODE
- Install flash to manage the flash messages if need be.
- Install all other dependencies as gotten from the requirements.txt file
- Run the app (run python app.py via terminal)

## Inspiration in creating the app
The inspiration for this pure water supply project stemmed from a personal experience and a desire to address challenges faced by one of the team members' father in managing his pure water company. His pure water company operates within a dynamic and demanding market, where efficiency, transparency, and customer satisfaction are pa
ramount. As a business owner, he faces numerous challenges in managing the day-to-day operations of the company, including order processing, delivery logistics, and financial management. Despite his best efforts, he continues to encounter inefficiencies and bottlenecks in the existing processes.

The idea took shape as we observed the growing trend of digital transformation across industries, where businesses were harnessing the power of technology to enhance efficiency, improve customer experience, and drive growth. Inspired by these developments, we embarked on a journey to develop an innovative solution tailored specifically to the needs of his pure water business. The app would serve as a centralized platform, offering insights and analytics to optimize operations, improve resource allocation, and enhance decision-making. With a bird's-eye view of the entire supply chain, he would have greater control and visibility, enabling him to address issues proactively and deliver exceptional service to customers. The project became more than just a technological endeavor; it was a testament to our commitment to innovation, entrepreneurship, and family legacy.

## MVP User Stories
- Customer
    - As a customer, I want to be able to request for water to be delivered to my location.
    - I should be able to see my delivery status and track requests based on phone number or name
- Factory Worker
    - As a factory worker, I should be able to view and edit customer request and update request status when the water has been delivered.
    - I should be able to add/edit packs/bags of water produced.
- Factory Owner / Manager
    - As a manager, I should have a dashboard that gives the reuests summary for the day.
    - I should be able to have a summarized view of production data for the day.
    - I should be able to view all outstanding requests that are yet to be actioned upon.
    - Register and login functualities for company.

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
    - Customers can lay complaints such as water not being delivered on time and any other thing?

- Water Company
    - Have a master page for company and ensure the company is the verified company.
    - Ability to know penetration rates and the orders (size) of business within areas.
    - Login capabilities is a must have.
    - Have the ability to manage accesses for factory workers.
    - Have the ability to manage cost price for the products.
    - Have a cost analysis and reporting template for water produced and sold.
    - Expenses management.

## Contribute
Contributions are always welcome!

## License
MIT License
