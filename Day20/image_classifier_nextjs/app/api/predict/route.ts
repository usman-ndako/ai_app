// import { NextResponse } from "next/server";

// export async function POST(request: Request) {
//   const { image } = await request.json();

//   // 🔮 Simulate AI prediction (mock)
//   const emotions = [
//     "Happy",
//     "Sad",
//     "Angry",
//     "Surprised",
//     "Fearful",
//     "Disgusted",
//     "Neutral",
//   ];
//   const randomEmotion =
//     emotions[Math.floor(Math.random() * emotions.length)];

//   return NextResponse.json({ prediction: randomEmotion });
// }


import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    const image = formData.get("image") as File;

    if (!image) {
      return NextResponse.json({ error: "No image uploaded" }, { status: 400 });
    }

    // Get backend URL from .env.local
    const backendUrl = process.env.NEXT_PUBLIC_API_URL;

    // Prepare data to send to FastAPI backend
    const uploadForm = new FormData();
    uploadForm.append("file", image);

    const response = await fetch(`${backendUrl}/predict/`, {
      method: "POST",
      body: uploadForm,
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`Backend Error: ${errText}`);
    }

    const result = await response.json();
    return NextResponse.json({ prediction: result.emotion });

  } catch (error: any) {
    console.error("Prediction error:", error);
    return NextResponse.json(
      { error: error.message || "Internal Server Error" },
      { status: 500 }
    );
  }
}
