# File Converter

A modern, professional file conversion application with a beautiful UI. Convert between various file formats including images, PDFs, and text documents.

## 🚀 Features

- **Image to PDF** - Convert images to PDF documents
- **PDF to Images** - Extract images from PDF files
- **Text to PDF** - Convert text files to formatted PDFs
- **PDF to Text** - Extract text content from PDFs
- **Modern UI** - Beautiful, responsive interface with smooth animations
- **Fast Processing** - Efficient conversion powered by Python backend
- **Secure** - Files are automatically cleaned up after conversion

## 📋 Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **npm** or **yarn**

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd fconverter
```

### 2. Backend Setup

```bash
cd server

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file and configure
cp .env.example .env
# Edit .env with your settings
```

### 3. Frontend Setup

```bash
cd fconverter

# Install dependencies
npm install

# Copy environment file and configure
cp .env.example .env
# Edit .env with your API URL
```

## 🚀 Running Locally

### Start the Backend

```bash
cd server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Start the Frontend

```bash
cd fconverter
npm run dev
```

The application will be available at `http://localhost:5173`

## 📦 Production Deployment

### Backend Deployment

1. **Set environment variables:**
   ```bash
   HOST=0.0.0.0
   PORT=8000
   DEBUG=False
   MAX_FILE_SIZE=10485760
   CLEANUP_AFTER_MINUTES=30
   ```

2. **Run with production server:**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

   Or use **Gunicorn** for better performance:
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

### Frontend Deployment

1. **Set production environment variable:**
   ```bash
   # In .env or .env.production
   VITE_API_BASE_URL=https://your-api-domain.com
   ```

2. **Build the application:**
   ```bash
   npm run build
   ```

3. **Deploy the `dist` folder** to your hosting service (Vercel, Netlify, etc.)

## 🌐 Environment Variables

### Backend (`server/.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Debug mode | `False` |
| `MAX_FILE_SIZE` | Max upload size in bytes | `10485760` (10MB) |
| `CLEANUP_AFTER_MINUTES` | File cleanup interval | `30` |

### Frontend (`fconverter/.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API URL | `http://localhost:8000` |

## 📁 Project Structure

```
fconverter/
├── fconverter/          # Frontend (React + TypeScript + Vite)
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── App.tsx      # Main application
│   │   └── index.css    # Styles
│   ├── .env.example     # Environment template
│   └── package.json
│
├── server/              # Backend (FastAPI + Python)
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── services/    # Conversion services
│   │   └── main.py      # FastAPI application
│   ├── uploads/         # Temporary uploads
│   ├── outputs/         # Conversion outputs
│   ├── .env.example     # Environment template
│   └── requirements.txt
│
└── .gitignore           # Git ignore rules
```

## 🔒 Security Notes

- Files are automatically deleted after the specified cleanup period
- Maximum file size limits prevent abuse
- CORS is configured for security
- Never commit `.env` files to version control

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🐛 Troubleshooting

### Backend Issues

- **Port already in use**: Change the `PORT` in `.env`
- **Module not found**: Ensure all dependencies are installed with `pip install -r requirements.txt`
- **Permission errors**: Check file permissions for `uploads/` and `outputs/` directories

### Frontend Issues

- **API connection failed**: Verify `VITE_API_BASE_URL` in `.env` matches your backend URL
- **Build errors**: Clear `node_modules` and reinstall with `npm install`
- **Environment variables not working**: Restart the dev server after changing `.env`

## 📞 Support

For issues and questions, please open an issue on GitHub.
