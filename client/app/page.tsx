"use client";
import { useState } from "react";
import { Textarea, Button } from "@nextui-org/react";

import { title, subtitle } from "@/components/primitives";

export default function SentimentAnalyzer() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);

  const analyzeSentiment = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ paragraph: text }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
      <div className="inline-block max-w-xl text-center justify-center">
        <h1 className={title({ color: "green" })}>Sentiment Analyzer for Business</h1>
        <br />
        <div className={subtitle({ class: "mt-4" })}>
          Simply enter the text you want to analyze in the textarea below and click on "Analyze."
        </div>
      </div>

      <div className="flex flex-col gap-3 w-full max-w-xl">
        <Textarea
          placeholder="Enter text to analyze"
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={5}
          className="w-full p-2 mt-4 border rounded"
        />
        <Button className="mt-4" onClick={analyzeSentiment} color="primary" auto>
          Analyze
        </Button>

        {result && (
          <div className="mt-6 p-4 border rounded shadow-lg w-full">
            <h2 className="text-2xl font-semibold text-blue-600 mb-4">Analysis Summary</h2>

            <div className="text-left space-y-3">
              <div className="border-b pb-2 mb-3">
                <h3 className="text-lg font-bold text-gray-700">Emoji & Sentiment Overview</h3>
                <p><strong>Total Emojis:</strong> {result["Total Emojis"]}</p>
                <p><strong>Overall Sentiment:</strong> {result["Overal Emoji Sentiment"]}</p>
              </div>

              <div className="border-b pb-2 mb-3">
                <h3 className="text-lg font-bold text-gray-700">Classified Sentences</h3>
                {result.classified_results.map((item, index) => (
                  <div key={index} className="mb-2">
                    <p><strong>Sentence:</strong> {item.Sentence}</p>
                    <p><strong>Type:</strong> {item.Type}</p>
                  </div>
                ))}
              </div>

              <div className="border-b pb-2 mb-3">
                <h3 className="text-lg font-bold text-gray-700">General Statements</h3>
                {result.general_statements.map((item, index) => (
                  <div key={index} className="mb-2">
                    <p><strong>Statement:</strong> {item["General Statement"]}</p>
                    <p><strong>Sentiment:</strong> {item.Sentiment}</p>
                    <p><strong>Recommendation:</strong> {item.Recommendation}</p>
                  </div>
                ))}
              </div>

              <div>
                <h3 className="text-lg font-bold text-gray-700">Financial Insights</h3>
                {result.recommendations.map((item, index) => (
                  <div key={index} className="mb-2">
                    <p><strong>Statement:</strong> {item["Financial Statement"]}</p>
                    <p><strong>Recommendation:</strong> {item.Recommendation}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
