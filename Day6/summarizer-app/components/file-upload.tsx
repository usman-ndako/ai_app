'use client';

import { useCallback, useState } from 'react';
import { Card } from '@/components/ui/card';
import { FiUpload, FiFile } from 'react-icons/fi';
import { toast } from 'sonner';
import mammoth from 'mammoth';

interface FileUploadProps {
  onFileRead: (text: string) => void;
}

export default function FileUpload({ onFileRead }: FileUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  const extractTextFromDocx = async (file: File): Promise<string> => {
    const arrayBuffer = await file.arrayBuffer();
    const result = await mammoth.extractRawText({ arrayBuffer });
    return result.value;
  };

  const extractTextFromPdf = async (file: File): Promise<string> => {
  try {
    // Dynamic import for PDF.js (client-side only)
    const pdfjsLib = await import('pdfjs-dist');
    
    // Use worker from unpkg CDN (more reliable than cdnjs)
    pdfjsLib.GlobalWorkerOptions.workerSrc = `https://unpkg.com/pdfjs-dist@${pdfjsLib.version}/build/pdf.worker.min.mjs`;

    const arrayBuffer = await file.arrayBuffer();
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    
    let fullText = '';
    
    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i);
      const textContent = await page.getTextContent();
      const pageText = textContent.items
        .map((item) => {
          // Check if the item has a 'str' property and it's a string
          if (typeof item === 'object' && item !== null && 'str' in item && typeof item.str === 'string') {
            return item.str;
          }
          return '';
        })
        .join(' ');
      fullText += pageText + '\n';
    }
    
    return fullText.trim();
  } catch (error) {
    console.error('PDF extraction error:', error);
    throw new Error('Failed to extract text from PDF');
  }
};

  const extractTextFromTxt = async (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target?.result as string);
      reader.onerror = reject;
      reader.readAsText(file);
    });
  };

  const handleFile = useCallback(
    async (file: File) => {
      const fileExtension = file.name.split('.').pop()?.toLowerCase();
      
      if (!['txt', 'docx', 'pdf'].includes(fileExtension || '')) {
        toast.error('Only TXT, DOCX, and PDF files are supported');
        return;
      }

      setIsProcessing(true);
      
      try {
        let text = '';
        
        switch (fileExtension) {
          case 'txt':
            text = await extractTextFromTxt(file);
            break;
          case 'docx':
            text = await extractTextFromDocx(file);
            toast.success('Word document processed successfully!');
            break;
          case 'pdf':
            text = await extractTextFromPdf(file);
            toast.success('PDF document processed successfully!');
            break;
          default:
            throw new Error('Unsupported file type');
        }

        onFileRead(text);
      } catch (error) {
        console.error('File processing error:', error);
        toast.error(`Failed to process ${fileExtension?.toUpperCase()} file. Please try another format.`);
      } finally {
        setIsProcessing(false);
      }
    },
    [onFileRead]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);

      const file = e.dataTransfer.files[0];
      if (file) {
        handleFile(file);
      }
    },
    [handleFile]
  );

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback(() => {
    setIsDragging(false);
  }, []);

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) {
        handleFile(file);
      }
    },
    [handleFile]
  );

  return (
    <Card
      className={`border-2 border-dashed transition-colors ${
        isDragging
          ? 'border-blue-500 bg-blue-50'
          : 'border-slate-300 hover:border-slate-400'
      }`}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
    >
      <label className="block p-8 cursor-pointer">
        <input
          type="file"
          accept=".txt,.docx,.pdf"
          onChange={handleFileInput}
          className="hidden"
          disabled={isProcessing}
        />
        <div className="flex flex-col items-center gap-3 text-center">
          <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
            {isProcessing ? (
              <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
            ) : isDragging ? (
              <FiFile className="w-6 h-6 text-blue-600" />
            ) : (
              <FiUpload className="w-6 h-6 text-blue-600" />
            )}
          </div>
          <div>
            <p className="font-medium text-slate-700">
              {isProcessing 
                ? 'Processing file...' 
                : isDragging 
                ? 'Drop file here' 
                : 'Click to upload or drag and drop'}
            </p>
            <p className="text-sm text-slate-500 mt-1">
              TXT, DOCX, or PDF files (max 10,000 characters)
            </p>
          </div>
        </div>
      </label>
    </Card>
  );
}
