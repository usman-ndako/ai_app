# AI Document Summarizer - Frontend

Professional Next.js frontend for the AI Document Summarizer API.

## 🚀 Features

### Core Functionality
- **5 Summary Types:** Executive, Legal, Technical, Financial, Standard
- **Multiple File Formats:** TXT, DOCX, PDF upload support
- **Drag & Drop:** Intuitive file upload interface
- **Real-time Processing:** Live API integration with loading states
- **Export Options:** Download summaries as TXT or JSON

### UI/UX Features
- **Modern SaaS Design:** Gradient accents, clean cards, professional styling
- **Responsive Design:** Works perfectly on desktop, tablet, and mobile
- **API Health Monitoring:** Real-time connection status indicator
- **Character Counter:** Progress bar showing 0/10,000 characters
- **Toast Notifications:** Clear feedback for all actions
- **Loading Skeletons:** Smooth loading experience
- **Error Handling:** Clear error messages with retry guidance

### User Experience
- **Copy to Clipboard:** One-click copy of summaries
- **Enter to Submit:** Quick keyboard submission
- **Performance Metrics:** Compression ratio, processing time displayed
- **File Processing:** Automatic text extraction from documents

## 🛠️ Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS 4
- **UI Components:** shadcn/ui
- **Icons:** react-icons
- **Notifications:** sonner (toast)
- **File Processing:** 
  - `mammoth` (DOCX)
  - `pdfjs-dist` (PDF)

## 📦 Installation
```bash
# Clone and navigate
cd day6/summarizer-app

# Install dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://127.0.0.1:8000" > .env.local

# Run development server
npm run dev
Visit http://localhost:3000
🔧 Configuration
Environment Variables
Create .env.local:
envNEXT_PUBLIC_API_URL=http://127.0.0.1:8000
For production:
envNEXT_PUBLIC_API_URL=https://your-api-domain.com
🏗️ Project Structure
summarizer-app/
├── app/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Main page
│   └── globals.css          # Global styles (Tailwind 4)
├── components/
│   ├── ui/                  # shadcn components
│   ├── summarizer-form.tsx  # Main form component
│   ├── result-display.tsx   # Results display
│   ├── file-upload.tsx      # File upload with drag-drop
│   ├── loading-skeleton.tsx # Loading state
│   └── api-health-indicator.tsx # API status
├── lib/
│   ├── types.ts             # TypeScript definitions
│   ├── api.ts               # API client
│   └── utils.ts             # Helper functions
└── public/                  # Static assets
🎨 Component Overview
Main Components
SummarizerForm

Text input with character limits
Summary type selector
File upload toggle
Submit button with loading states

ResultDisplay

Summary card with type badge
Copy/Export buttons
Performance metrics grid
Responsive layout

FileUpload

Drag and drop interface
Multi-format support (TXT, DOCX, PDF)
Processing states
Error handling

ApiHealthIndicator

Real-time API status
Auto-refresh every 30s
Visual status indicators

🧪 Testing
Manual Testing Checklist
Text Input:

 Type directly in textarea
 Character counter updates
 Submit with Enter key
 Clear button works

File Upload:

 Upload TXT file
 Upload DOCX file
 Upload PDF file
 Drag and drop works

Summary Generation:

 All 5 summary types work
 Loading skeleton appears
 Results display correctly
 Metrics are accurate

Export Features:

 Copy to clipboard
 Export as TXT
 Export as JSON

Error Handling:

 Empty text validation
 API offline handling
 File upload errors
 Network errors

📱 Responsive Design
Breakpoints:

Mobile: < 768px
Tablet: 768px - 1024px
Desktop: > 1024px

Features:

Fluid typography scaling
Responsive grid layouts
Touch-friendly buttons
Optimized file upload on mobile

🚀 Deployment
Build for Production
bashnpm run build
npm start
Deploy to Vercel
bash# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
Set environment variable in Vercel dashboard:

NEXT_PUBLIC_API_URL: Your production API URL

🔗 API Integration
The frontend connects to the FastAPI backend:
Endpoints Used:

GET / - Health check
POST /summarize - Generate summary
GET /summary-types - Get available types

Request Format:
typescript{
  "text": "Document content...",
  "summary_type": "executive"
}
Response Format:
typescript{
  "success": true,
  "summary": "Generated summary...",
  "metadata": {
    "summary_type": "executive",
    "original_length": 698,
    "summary_length": 255,
    "compression_ratio": "36.5%",
    "processing_time_seconds": 0.87,
    "model_version": "sshleifer/distilbart-cnn-12-6"
  }
}
💡 Usage Examples
Basic Usage

Paste or type document text
Select summary type
Click "Generate Summary"
Copy or export results

File Upload

Click "Upload File" button
Select TXT/DOCX/PDF file
Text auto-populates
Generate summary

Export Options

Copy: Quick clipboard copy
TXT: Download formatted text file
JSON: Download structured data

🎯 Business Value
Time Savings:

Executives: Get strategic insights in 30 seconds
Legal teams: Review contracts 2.5 hours faster
Finance teams: Extract metrics instantly

ROI Example:

Law firm processing 40 docs/month
Time saved: 2.5 hours × $300/hr × 40
Annual savings: $360,000

📊 Performance
Metrics:

Initial load: < 1s
API response: 0.5-2s (CPU)
File processing: 1-3s
Export operations: Instant

🔒 Security

No data stored locally
API calls over HTTPS (production)
File processing client-side
No cookies or tracking

🐛 Troubleshooting
API Connection Failed:

Ensure backend is running on port 8000
Check CORS is enabled on API
Verify NEXT_PUBLIC_API_URL is correct

File Upload Issues:

Only TXT, DOCX, PDF supported
Max 10,000 characters
Check file isn't corrupted

PDF Not Loading:

Worker script loads from unpkg CDN
Check internet connection
Try different PDF if corrupted

📝 Day 6 Deliverables
✅ Complete Next.js Application

Professional UI with Modern SaaS design
Full API integration
Multiple file format support
Export functionality
Responsive design
Production-ready code

🔮 Future Enhancements

 Dark mode toggle
 Multi-document comparison
 Summary history
 User accounts
 Batch processing
 Custom summary lengths
 More file formats (RTF, HTML)
 OCR for scanned PDFs

👤 Author
Built as part of 60-Day AI Entrepreneur Intensive - Day 6
📄 License
Proprietary - MVP Project