
# The Finalyzer

## Comprehensive Financial Analysis Tool

The Finalyzer is an advanced financial analysis tool developed using Python, HTML, CSS, Bootstrap, and Flask. It performs RSI Index calculations and provides related news provision, integrating real-time financial data from the Yahoo Finance API.

### Features
- **Real-time Financial Data**: Integrates Yahoo Finance API to fetch real-time financial data.
- **RSI Index Calculation**: Calculates the Relative Strength Index (RSI) to help identify overbought or oversold conditions.
- **Comprehensive Analysis**: Provides detailed financial metrics including market cap, P/E ratio, EPS, and more.
- **User-friendly Interface**: Implemented using Flask and Jinja for seamless user experience.
- **Dynamic Content**: Utilizes Bootstrap for responsive design and dynamic content rendering.

### How to Run the Project
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/temilola23/The-Finalyzer.git
   cd The-Finalyzer/final
   ```

2. **Install Dependencies**:
   Ensure you have Python and pip installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   Navigate to the `final` directory and run the Flask application:
   ```bash
   cd final
   python app.py
   ```

4. **Access the Application**:
   Open your web browser and go to `http://127.0.0.1:5000` to access The Finalyzer.

### Project Structure
- **app.py**: Main Flask application file.
- **main.py**: Contains the core logic for interacting with the Yahoo Finance API and performing calculations.
- **information.py**: Defines key metrics used in the application.
- **templates/**: Contains the HTML templates for the Flask application.
  - **index.html**: Homepage template.
  - **about.html**: About Us page template.
  - **contact.html**: Contact Us page template.
  - **more.html**: More Information page template.
  - **privacy_policy.html**: Privacy Policy page template.
  - **stock_analysis.html**: Stock Analysis page template.
  - **ticker_info.html**: Ticker Information page template.
  - **view_contacts.html**: View Contacts page template.
- **static/**: Contains static files such as CSS, images, and JavaScript.
  - **css/**: Contains CSS stylesheets.
    - **style.css**: Main stylesheet for the project.
  - **images/**: Contains images used in the project.

### Code Overview

#### app.py
This is the main file for the Flask application. It defines the routes, handles requests, and renders the templates.

#### main.py
This file contains the core logic for interacting with the Yahoo Finance API and performing calculations. It defines the `Stock` class, which retrieves and processes financial data for a given ticker.

#### information.py
This file defines key metrics used in the application. It provides descriptions for various financial metrics.

### Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request. We welcome all contributions!

### Contact
For updates or questions about this project, please contact:
- Temilola Olowolayemo (Project Lead) - temilola@uni.minerva.edu

### Contributors
- Temilola Olowolayemo - Project Lead, Core Developer
- Max Kainamura - Chief Economist, API Integration Specialist
- Mofetoluwa Sam-Adelusimo - Chief Operating Officer, UI/UX Designer

### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgements
We would like to thank the following resources and libraries that made this project possible:
- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Yahoo Finance API](https://www.yahoofinanceapi.com/)
