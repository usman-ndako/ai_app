// "use client";

// import { useEffect, useState } from "react";

// interface FAQ {
//   question: string;
//   answer: string;
// }

// interface FAQForm {
//   question: string;
//   answer: string;
// }

// export default function FAQManager() {
//   const [faqs, setFaqs] = useState<FAQ[]>([]);
//   const [faqForm, setFAQForm] = useState<FAQForm>({ question: "", answer: "" });
//   const [loading, setLoading] = useState(false);
//   const [formLoading, setFormLoading] = useState(false);
//   const [uploadLoading, setUploadLoading] = useState(false);
//   const [success, setSuccess] = useState("");

//   const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

//   // Fetch existing FAQs on load
//   useEffect(() => {
//     fetchFaqs();
//   }, []);

//   const fetchFaqs = async () => {
//     setLoading(true);
//     try {
//       const res = await fetch(`${API_URL}/get_faqs`);
//       if (res.ok) {
//         const data = await res.json();
//         setFaqs(data.faqs);
//       }
//     } catch (error) {
//       console.error("Error fetching FAQs:", error);
//       setSuccess("Failed to fetch FAQs.");
//     } finally {
//       setLoading(false);
//     }
//   };

//   const addFAQ = async (form: FAQForm) => {
//     if (!form.question.trim() || !form.answer.trim()) return;

//     setFormLoading(true);
//     setSuccess("");

//     try {
//       const res = await fetch(`${API_URL}/add_faq`, {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify(form),
//       });

//       if (!res.ok) {
//         const errorData = await res.json();
//         throw new Error(errorData.detail || "Failed to add FAQ.");
//       }

//       const data = await res.json();
//       console.log("FAQ add response:", data);

//       setSuccess(`✅ ${data.message} Total FAQs now: ${data.total_faqs}`);
//       setFAQForm({ question: "", answer: "" });

//       // Refresh list
//       fetchFaqs();

//     } catch (error) {
//       console.error("Error adding FAQ:", error);
//       // Type guard for error.message
//       const errorMessage = error instanceof Error ? error.message : "An unknown error occurred.";
//       setSuccess(`❌ ${errorMessage}`);
//     } finally {
//       setFormLoading(false);
//     }
//   };

//   const uploadCSV = async (event: React.ChangeEvent<HTMLInputElement>) => {
//     const file = event.target.files?.[0];
//     if (!file) return;

//     if (!file.name.endsWith('.csv')) {
//       setSuccess("❌ Only CSV files are allowed.");
//       return;
//     }

//     const formData = new FormData();
//     formData.append('file', file);

//     setUploadLoading(true);
//     setSuccess("");

//     try {
//       const res = await fetch(`${API_URL}/upload_faq_csv`, {
//         method: "POST",
//         body: formData,
//       });

//       if (!res.ok) {
//         const errorData = await res.json();
//         throw new Error(errorData.detail || "Failed to upload CSV.");
//       }

//       const data = await res.json();
//       console.log("CSV upload response:", data);

//       setSuccess(`✅ ${data.message} Total FAQs now: ${data.total_faqs}`);

//       // Reset file input
//       event.target.value = '';

//       // Refresh list
//       fetchFaqs();

//     } catch (error) {
//       console.error("Error uploading CSV:", error);
//       // Type guard for error.message
//       const errorMessage = error instanceof Error ? error.message : "An unknown error occurred.";
//       setSuccess(`❌ ${errorMessage}`);
//     } finally {
//       setUploadLoading(false);
//     }
//   };

//   const handleSubmit = (e: React.FormEvent) => {
//     e.preventDefault();
//     addFAQ(faqForm);
//   };

//   return (
//     <div className="min-h-screen bg-gray-50 py-8">
//       <div className="max-w-4xl mx-auto px-6">
//         <div className="text-center mb-8">
//           <h1 className="text-3xl font-bold text-gray-800">FAQ Manager</h1>
//           <p className="text-gray-600 mt-2">Add new FAQs via form or CSV upload (non-technical users welcome!)</p>
//         </div>

//         {/* Manual Add FAQ Form */}
//         <div className="bg-white border rounded-2xl shadow-lg p-6 mb-6">
//           <h2 className="text-xl font-semibold mb-4">Add Single FAQ (Manual Entry)</h2>
//           <form onSubmit={handleSubmit} className="space-y-4">
//             <input
//               type="text"
//               placeholder="Enter question (e.g., What is your return policy?)"
//               className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-green-500"
//               value={faqForm.question}
//               onChange={(e) => setFAQForm({ ...faqForm, question: e.target.value })}
//               required
//             />
//             <textarea
//               placeholder="Enter answer (e.g., We offer 30-day returns...)"
//               className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-green-500 resize-none h-24"
//               value={faqForm.answer}
//               onChange={(e) => setFAQForm({ ...faqForm, answer: e.target.value })}
//               required
//             />
//             <button
//               type="submit"
//               disabled={formLoading || !faqForm.question.trim() || !faqForm.answer.trim()}
//               className="w-full bg-green-500 text-white py-3 rounded-lg hover:bg-green-600 transition disabled:opacity-50 font-medium"
//             >
//               {formLoading ? "Adding..." : "Add FAQ"}
//             </button>
//           </form>
//         </div>

//         {/* CSV Upload Section */}
//         <div className="bg-white border rounded-2xl shadow-lg p-6 mb-8">
//           <h2 className="text-xl font-semibold mb-4">Bulk Add FAQs (CSV Upload)</h2>
//           <p className="text-sm text-gray-600 mb-4">Upload a CSV with columns: <code>question</code> and <code>answer</code>.</p>
//           <input
//             type="file"
//             accept=".csv"
//             onChange={uploadCSV}
//             disabled={uploadLoading}
//             className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
//           />
//           {uploadLoading && <p className="text-sm text-blue-600 mt-2">Uploading...</p>}
//         </div>

//         {success && (
//           <div className={`mb-6 p-4 rounded-lg text-sm ${
//             success.includes("✅") ? "bg-green-50 text-green-700 border border-green-200" : "bg-red-50 text-red-700 border border-red-200"
//           }`}>
//             {success}
//           </div>
//         )}

//         {/* Existing FAQs List */}
//         <div className="bg-white border rounded-2xl shadow-lg p-6">
//           <h2 className="text-xl font-semibold mb-4">Current FAQs ({faqs.length})</h2>
//           {loading ? (
//             <p className="text-gray-500">Loading...</p>
//           ) : faqs.length === 0 ? (
//             <p className="text-gray-500">No FAQs yet. Add some above!</p>
//           ) : (
//             <div className="space-y-4 max-h-96 overflow-y-auto">
//               {faqs.map((faq, idx) => (
//                 <div key={idx} className="border-l-4 border-green-500 pl-4 pb-4">
//                   <h3 className="font-medium text-gray-800 mb-1">{faq.question}</h3>
//                   <p className="text-gray-600 text-sm">{faq.answer}</p>
//                 </div>
//               ))}
//             </div>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// }

"use client";

import { useEffect, useState } from "react";

interface FAQ {
  question: string;
  answer: string;
}

interface FAQForm {
  question: string;
  answer: string;
}

export default function FAQManager() {
  const [faqs, setFaqs] = useState<FAQ[]>([]);
  const [faqForm, setFAQForm] = useState<FAQForm>({ question: "", answer: "" });
  const [loading, setLoading] = useState(false);
  const [formLoading, setFormLoading] = useState(false);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [success, setSuccess] = useState("");

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

  // Fetch existing FAQs on load
  useEffect(() => {
    fetchFaqs();
  }, []);

  const fetchFaqs = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/get_faqs`);
      if (res.ok) {
        const data = await res.json();
        setFaqs(data.faqs);
      }
    } catch (error) {
      console.error("Error fetching FAQs:", error);
      setSuccess("Failed to fetch FAQs.");
    } finally {
      setLoading(false);
    }
  };

  const addFAQ = async (form: FAQForm) => {
    if (!form.question.trim() || !form.answer.trim()) return;

    setFormLoading(true);
    setSuccess("");

    try {
      const res = await fetch(`${API_URL}/add_faq`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Failed to add FAQ.");
      }

      const data = await res.json();
      console.log("FAQ add response:", data);

      if (!data.success) {
        // Duplicate case - show as info, not error
        setSuccess(`ℹ️ ${data.message}`);
        return;
      }

      setSuccess(`✅ ${data.message} Total FAQs now: ${data.total_faqs}`);
      setFAQForm({ question: "", answer: "" });

      // Refresh list
      fetchFaqs();

    } catch (error) {
      console.error("Error adding FAQ:", error);
      // Type guard for error.message
      const errorMessage = error instanceof Error ? error.message : "An unknown error occurred.";
      setSuccess(`❌ ${errorMessage}`);
    } finally {
      setFormLoading(false);
    }
  };

  const uploadCSV = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (!file.name.endsWith('.csv')) {
      setSuccess("❌ Only CSV files are allowed.");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setUploadLoading(true);
    setSuccess("");

    try {
      const res = await fetch(`${API_URL}/upload_faq_csv`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json();
        if (res.status === 400) {
          // Duplicate case - show as info, not error
          setSuccess(`ℹ️ ${errorData.detail}`);
          return;
        }
        throw new Error(errorData.detail || "Failed to upload CSV.");
      }

      const data = await res.json();
      console.log("CSV upload response:", data);

      setSuccess(`✅ ${data.message} Total FAQs now: ${data.total_faqs}`);

      // Reset file input
      event.target.value = '';

      // Refresh list
      fetchFaqs();

    } catch (error) {
      console.error("Error uploading CSV:", error);
      // Type guard for error.message
      const errorMessage = error instanceof Error ? error.message : "An unknown error occurred.";
      setSuccess(`❌ ${errorMessage}`);
    } finally {
      setUploadLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    addFAQ(faqForm);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-6">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">FAQ Manager</h1>
          <p className="text-gray-600 mt-2">Add new FAQs via form or CSV upload (non-technical users welcome!)</p>
        </div>

        {/* Manual Add FAQ Form */}
        <div className="bg-white border rounded-2xl shadow-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Add Single FAQ (Manual Entry)</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="text"
              placeholder="Enter question (e.g., What is your return policy?)"
              className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-green-500"
              value={faqForm.question}
              onChange={(e) => setFAQForm({ ...faqForm, question: e.target.value })}
              required
            />
            <textarea
              placeholder="Enter answer (e.g., We offer 30-day returns...)"
              className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-green-500 resize-none h-24"
              value={faqForm.answer}
              onChange={(e) => setFAQForm({ ...faqForm, answer: e.target.value })}
              required
            />
            <button
              type="submit"
              disabled={formLoading || !faqForm.question.trim() || !faqForm.answer.trim()}
              className="w-full bg-green-500 text-white py-3 rounded-lg hover:bg-green-600 transition disabled:opacity-50 font-medium"
            >
              {formLoading ? "Adding..." : "Add FAQ"}
            </button>
          </form>
        </div>

        {/* CSV Upload Section */}
        <div className="bg-white border rounded-2xl shadow-lg p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Bulk Add FAQs (CSV Upload)</h2>
          <p className="text-sm text-gray-600 mb-4">Upload a CSV with columns: <code>question</code> and <code>answer</code>.</p>
          <input
            type="file"
            accept=".csv"
            onChange={uploadCSV}
            disabled={uploadLoading}
            className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          {uploadLoading && <p className="text-sm text-blue-600 mt-2">Uploading...</p>}
        </div>

        {success && (
          <div className={`mb-6 p-4 rounded-lg text-sm ${
            success.startsWith("✅") ? "bg-green-50 text-green-700 border border-green-200" :
            success.startsWith("ℹ️") ? "bg-yellow-50 text-yellow-700 border border-yellow-200" :
            "bg-red-50 text-red-700 border border-red-200"
          }`}>
            {success}
          </div>
        )}

        {/* Existing FAQs List */}
        <div className="bg-white border rounded-2xl shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Current FAQs ({faqs.length})</h2>
          {loading ? (
            <p className="text-gray-500">Loading...</p>
          ) : faqs.length === 0 ? (
            <p className="text-gray-500">No FAQs yet. Add some above!</p>
          ) : (
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {faqs.map((faq, idx) => (
                <div key={idx} className="border-l-4 border-green-500 pl-4 pb-4">
                  <h3 className="font-medium text-gray-800 mb-1">{faq.question}</h3>
                  <p className="text-gray-600 text-sm">{faq.answer}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}