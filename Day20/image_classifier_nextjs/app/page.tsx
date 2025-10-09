// "use client";

// import { useState } from "react";
// import { motion } from "framer-motion";
// import { Upload, Image as ImageIcon, Loader2 } from "lucide-react";

// export default function Home() {
//   const [image, setImage] = useState<string | null>(null);
//   const [loading, setLoading] = useState(false);
//   const [result, setResult] = useState<string | null>(null);

//   const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
//     const file = e.target.files?.[0];
//     if (!file) return;

//     setResult(null);
//     const reader = new FileReader();
//     reader.onloadend = () => setImage(reader.result as string);
//     reader.readAsDataURL(file);
//   };

//   const handlePredict = async () => {
//     if (!image) return;
//     setLoading(true);

//     // 🔮 Mock API call
//     const res = await fetch("/api/predict", {
//       method: "POST",
//       body: JSON.stringify({ image }),
//     });

//     const data = await res.json();
//     setResult(data.prediction);
//     setLoading(false);
//   };

//   return (
//     <main className="flex min-h-screen flex-col items-center justify-center bg-gray-50 p-6">
//       <motion.div
//         initial={{ opacity: 0, y: 40 }}
//         animate={{ opacity: 1, y: 0 }}
//         transition={{ duration: 0.5 }}
//         className="w-full max-w-md rounded-2xl bg-white shadow-lg p-6 text-center"
//       >
//         <h1 className="text-2xl font-semibold mb-4 text-gray-800">
//           AI Emotion Classifier 🎭
//         </h1>
//         <p className="text-gray-500 mb-6">
//           Upload an image to predict facial emotion using AI.
//         </p>

//         <label
//           htmlFor="file-upload"
//           className="cursor-pointer flex flex-col items-center justify-center border-2 border-dashed border-gray-300 rounded-xl p-8 hover:border-indigo-400 transition"
//         >
//           {image ? (
//             <img
//               src={image}
//               alt="Uploaded"
//               className="rounded-xl w-full object-cover h-56 mb-4"
//             />
//           ) : (
//             <>
//               <Upload className="w-10 h-10 text-gray-400 mb-2" />
//               <span className="text-gray-500">Click or drag to upload</span>
//             </>
//           )}
//           <input
//             id="file-upload"
//             type="file"
//             accept="image/*"
//             className="hidden"
//             onChange={handleUpload}
//           />
//         </label>

//         {image && (
//           <button
//             onClick={handlePredict}
//             disabled={loading}
//             className="mt-6 w-full bg-indigo-600 text-white py-2 rounded-xl hover:bg-indigo-700 transition flex items-center justify-center gap-2"
//           >
//             {loading ? (
//               <>
//                 <Loader2 className="animate-spin w-5 h-5" /> Analyzing...
//               </>
//             ) : (
//               <>
//                 <ImageIcon className="w-5 h-5" /> Analyze Emotion
//               </>
//             )}
//           </button>
//         )}

//         {result && (
//           <motion.div
//             initial={{ opacity: 0, y: 10 }}
//             animate={{ opacity: 1, y: 0 }}
//             className="mt-6 p-4 rounded-xl bg-green-50 border border-green-200 text-green-700 font-medium"
//           >
//             Emotion Detected: <span className="font-bold">{result}</span>
//           </motion.div>
//         )}
//       </motion.div>

//       <footer className="mt-8 text-gray-400 text-sm">
//         Built with ❤️ on Day 20 — AI Frontend Integration
//       </footer>
//     </main>
//   );
// }


"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Upload, Image as ImageIcon, Loader2 } from "lucide-react";

export default function Home() {
  const [image, setImage] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);

  const handleUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) return;

    setFile(selectedFile);
    setResult(null);

    const reader = new FileReader();
    reader.onloadend = () => setImage(reader.result as string);
    reader.readAsDataURL(selectedFile);
  };

  const handlePredict = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("image", file);

    try {
      const res = await fetch("/api/predict", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResult(data.prediction || data.error || "Error occurred");
    } catch (error) {
      console.error(error);
      setResult("Failed to connect to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-gray-50 to-gray-100 p-6">
      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="relative w-full max-w-md rounded-2xl bg-white shadow-2xl p-6 text-center"
      >
        <h1 className="text-3xl font-bold mb-4 text-gray-800">
          AI Emotion Classifier 🎭
        </h1>
        <p className="text-gray-500 mb-6">
          Upload an image to detect facial emotion using AI.
        </p>

        <label
          htmlFor="file-upload"
          className="cursor-pointer flex flex-col items-center justify-center border-2 border-dashed border-gray-300 rounded-xl p-8 hover:border-indigo-400 transition"
        >
          {image ? (
            <img
              src={image}
              alt="Uploaded"
              className="rounded-xl w-full object-cover h-56 mb-4 shadow-sm"
            />
          ) : (
            <>
              <Upload className="w-10 h-10 text-gray-400 mb-2" />
              <span className="text-gray-500">Click or drag to upload</span>
            </>
          )}
          <input
            id="file-upload"
            type="file"
            accept="image/*"
            className="hidden"
            onChange={handleUpload}
          />
        </label>

        {image && (
          <div className="relative mt-6">
            {loading && (
              <motion.div
                className="absolute inset-0 flex items-center justify-center"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                <motion.div
                  className="w-16 h-16 rounded-full border-4 border-indigo-300 border-t-indigo-600"
                  animate={{ rotate: 360 }}
                  transition={{
                    repeat: Infinity,
                    duration: 1,
                    ease: "linear",
                  }}
                />
              </motion.div>
            )}

            <button
              onClick={handlePredict}
              disabled={loading}
              className={`relative w-full bg-indigo-600 text-white py-3 rounded-xl hover:bg-indigo-700 transition flex items-center justify-center gap-2 shadow-md ${
                loading ? "opacity-70 cursor-not-allowed" : ""
              }`}
            >
              {loading ? (
                <>
                  <Loader2 className="animate-spin w-5 h-5" /> Analyzing...
                </>
              ) : (
                <>
                  <ImageIcon className="w-5 h-5" /> Analyze Emotion
                </>
              )}
            </button>

            {/* Subtle glow animation when analyzing */}
            {loading && (
              <motion.div
                className="absolute -inset-1 rounded-xl bg-indigo-400 blur-2xl opacity-30"
                animate={{ scale: [1, 1.05, 1], opacity: [0.2, 0.4, 0.2] }}
                transition={{ repeat: Infinity, duration: 1.6, ease: "easeInOut" }}
              />
            )}
          </div>
        )}

        {result && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`mt-8 p-4 rounded-xl border text-lg font-medium ${
              result.includes("Error")
                ? "bg-red-50 border-red-200 text-red-700"
                : "bg-green-50 border-green-200 text-green-700"
            }`}
          >
            {result.includes("Error") ? (
              <>⚠️ {result}</>
            ) : (
              <>
                Emotion Detected:{" "}
                <span className="font-bold text-green-800">{result}</span>
              </>
            )}
          </motion.div>
        )}
      </motion.div>

      <footer className="mt-8 text-gray-400 text-sm">
        Built with ❤️ on <span className="font-semibold">Day 20</span> — AI
        Frontend Integration
      </footer>
    </main>
  );
}
