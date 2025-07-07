# 60 Days of Madonna

A serverless web application that delivers a different Madonna song each day for 60 days, celebrating the Queen of Pop's incredible musical catalog.

## 🎵 Live Demo

Visit: [https://60daysofmadonna.com](https://60daysofmadonna.com)

## 📖 About

60 Days of Madonna is a celebration project that provides users with a unique Madonna song each day. Users are tracked via cookies, ensuring they receive a new song daily while keeping track of their previous songs and day count.

### Features

- 🎶 **Daily Song**: Get a different Madonna song each day
- 📊 **Progress Tracking**: See your current day count (up to 60 days)
- 📝 **Song History**: View all your previous songs
- 🍪 **User Persistence**: Cookie-based user tracking
- 🔒 **HTTPS Secure**: Fully encrypted website and API
- 📱 **Responsive Design**: Works on all devices

## 🏗️ Architecture

This is a fully serverless application built on AWS:

### Frontend
- **S3**: Static website hosting
- **CloudFront**: HTTPS delivery and global CDN
- **Route53**: DNS management

### Backend
- **API Gateway**: RESTful API with custom domain
- **Lambda**: Serverless compute (Python 3.9)
- **DynamoDB**: User data and song history storage

### Security
- **ACM**: SSL/TLS certificates
- **CORS**: Properly configured cross-origin requests
- **IAM**: Secure access controls

## 🚀 API Endpoints

### Base URL
```
https://api.60daysofmadonna.com/prod
```

### Endpoints

#### Get Song of the Day
```http
GET /madz_get_a_song
```
Returns a song for the current user, creates new user if needed.

#### Get All Available Songs
```http
GET /madz_get_all_songs
```
Returns the complete list of Madonna songs.

#### Get User's Song History
```http
GET /madz_get_all_my_songs
```
Returns all songs the user has received.

#### Get User's Day Count
```http
GET /madz_get_my_day_count
```
Returns the user's current day count.

#### Reset User Progress
```http
GET /madz_reset_my_songs
```
Resets the user's progress to start over.

#### Create New User
```http
GET /madz_create_new_user
```
Manually creates a new user (normally done automatically).

## 📁 Project Structure

```
madonna_serverless/
├── README.md
├── s3/                          # Website files
│   ├── index.html              # Main website
│   ├── assets/                 # CSS and other assets
│   └── images/                 # Images and favicon
├── lambda_functions/           # Lambda function code
│   ├── madz_get_a_song_lambda.py
│   ├── madz_get_all_songs_lambda.py
│   ├── madz_get_all_my_songs_lambda.py
│   ├── madz_get_my_day_count_lambda.py
│   ├── madz_reset_my_songs_lambda.py
│   └── madz_create_new_user_lambda.py
├── config/                     # API Gateway configurations
│   ├── application.json
│   ├── mappings.json
│   └── swagger files
└── deployment/                 # Deployment scripts and docs
    └── infrastructure.md
```

## 🛠️ Local Development

### Prerequisites
- Python 3.9+
- AWS CLI configured
- Node.js (for local testing)

### Setup
1. Clone the repository
```bash
git clone <your-repo-url>
cd madonna_serverless
```

2. Install Python dependencies
```bash
pip install boto3 flask flask-cors
```

3. Set up local environment variables
```bash
export ENV=local
```

### Testing Lambda Functions Locally
```bash
cd lambda_functions
python madz_get_a_song_lambda.py
```

## 🚀 Deployment

### AWS Resources Required
- S3 bucket for website hosting
- CloudFront distribution
- API Gateway
- Lambda functions
- DynamoDB table
- Route53 hosted zone
- ACM SSL certificates

### Deployment Steps

1. **Deploy Lambda Functions**
```bash
# Package and deploy each function
zip lambda_function.zip madz_get_a_song_lambda.py
aws lambda update-function-code --function-name madz_get_a_song --zip-file fileb://lambda_function.zip
```

2. **Deploy Website**
```bash
aws s3 sync s3/ s3://your-bucket-name/
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
```

3. **Configure API Gateway**
- Import swagger configuration
- Deploy to production stage
- Set up custom domain

See `deployment/infrastructure.md` for detailed deployment instructions.

## 🎨 Technologies Used

### Frontend
- **HTML5/CSS3**: Modern web standards
- **JavaScript (ES6)**: AJAX API calls and DOM manipulation
- **Split Template**: Responsive design framework

### Backend
- **Python 3.9**: Lambda runtime
- **boto3**: AWS SDK for Python
- **JSON**: Data interchange format

### AWS Services
- **Lambda**: Serverless compute
- **API Gateway**: RESTful API
- **DynamoDB**: NoSQL database
- **S3**: Object storage and website hosting
- **CloudFront**: Content delivery network
- **Route53**: DNS service
- **ACM**: SSL certificate management
- **IAM**: Identity and access management

## 🔒 Security Features

- **HTTPS Everywhere**: All traffic encrypted in transit
- **CORS Protection**: Properly configured cross-origin requests
- **Cookie Security**: Secure cookie handling with proper expiration
- **IAM Roles**: Principle of least privilege access
- **API Rate Limiting**: Built-in API Gateway throttling

## 📊 Song Database

The application includes 306 Madonna songs spanning her entire career:
- Studio albums
- Singles
- B-sides
- Soundtrack contributions
- Evita musical numbers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎤 Acknowledgments

- **Madonna**: For an incredible 40+ year career and amazing music
- **Split Template**: By One Page Love for the responsive design
- **AWS**: For providing the serverless infrastructure
- **Community**: For testing and feedback

## 📧 Contact

- **Website**: [https://60daysofmadonna.com](https://60daysofmadonna.com)
- **API**: [https://api.60daysofmadonna.com](https://api.60daysofmadonna.com)

---

*Made with ❤️ for Madonna fans everywhere*