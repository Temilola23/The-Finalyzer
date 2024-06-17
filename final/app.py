from flask import Flask, render_template, request, redirect, url_for, flash
from main import Stock, Ticker, get_tickers_from_screeners
import locale
import warnings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# In-memory storage for contact form submissions
contact_submissions = []

# Function to send email notifications for contact form submissions
def send_email(name, email, message):
    try:
        sender_email = "your_email@example.com"
        receiver_email = "temilola@uni.minerva.edu"
        password = "your_email_password"

        # Create email content
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "New Contact Form Submission"

        body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        msg.attach(MIMEText(body, 'plain'))

        # Send email using SMTP server
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for the more page
@app.route('/more')
def more():
    return render_template('more.html')

# Route for the contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for the privacy policy page
@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')

# Route for selecting a ticker and redirecting to the ticker information page
@app.route('/select_ticker', methods=['POST'])
def select_ticker():
    ticker_symbol = request.form['ticker']
    return redirect(url_for('show_ticker_info', ticker=ticker_symbol))

# Route for displaying ticker information
@app.route('/ticker/<ticker>')
def show_ticker_info(ticker):
    stock_input = Ticker(ticker)
    stock_obj = Stock(stock_input, ticker)
    data = {
        'name': stock_obj.name,
        'industry': stock_obj.industry,
        'current_price': stock_obj.current_price,
        'fifty_two_week_high': stock_obj.fifty_two_week_high,
        'fifty_two_week_low': stock_obj.fifty_two_week_low,
        'capitalization': stock_obj.capitalization,
        'debt_to_equity_ratio': stock_obj.debt_to_equity_ratio,
        'price_to_earnings': stock_obj.price_to_earnings,
        'enterprise_value': stock_obj.enterprise_value,
        'earnings_per_share': stock_obj.earnings_per_share,
        'dividend_yield': stock_obj.dividend_yield,
        'beta': stock_obj.beta,
        'currency': stock_obj.currency
    }
    return render_template('ticker_info.html', ticker=ticker, data=data)

# Route for stock analysis
@app.route('/stock_analysis', methods=['GET', 'POST'])
def stock_analysis():
    tickers = get_tickers_from_screeners()  # Fetch the list of tickers
    data = {}
    if request.method == 'POST':
        ticker = request.form['ticker']
        action = request.form['action']
        period = int(request.form.get('period', 15))  # Get period from form or default to 15
        stock_input = Ticker(ticker)
        stock_obj = Stock(stock_input, ticker)

        data['ticker'] = ticker
        if action == 'rsi':
            data['rsi'] = stock_obj.get_rsi(period)
        elif action == 'important_info':
            data['important_info'] = stock_obj.get_most_important_info()
        elif action == 'financial_info':
            data['financial_info'] = stock_obj.get_all_financial_info()
        elif action == 'corporate_events':
            num_events = int(request.form.get('num_events', 5))
            data['corporate_events'] = stock_obj.get_corporate_events(num_events)

        return render_template('stock_analysis.html', tickers=tickers, data=data)
    return render_template('stock_analysis.html', tickers=tickers)

# Route for handling contact form submissions
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Store the submission in the in-memory dictionary
    contact_submissions.append({
        'name': name,
        'email': email,
        'message': message
    })

    # Send email notification
    send_email(name, email, message)

    flash('Your message has been submitted successfully!', 'success')
    return redirect(url_for('contact'))

# Route for viewing contact submissions
@app.route('/view_contacts')
def view_contacts():
    return render_template('view_contacts.html', contacts=contact_submissions)

if __name__ == '__main__':
    app.run(debug=True)
