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
      <div className="inline-block max-w-3xl text-center justify-center">
        <h1 className={title({ color: "green" })}>Sentiment Analyzer for Business</h1>
        <br />
        <div className={subtitle({ class: "mt-4" })}>
          Simply enter the text you want to analyze in the textarea below and click on "Analyze."
        </div>
      </div>

      <div className="flex flex-col gap-3 w-full max-w-4xl">
        <Textarea
          placeholder="Enter text to analyze"
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={5}
          className="w-full p-2 mt-4 border rounded"
        />
        <Button className="mt-4" onClick={analyzeSentiment} color="primary" auto >
          Analyze
        </Button>

        {result && (
          <div className="mt-6 p-6 border rounded shadow-lg w-full max-w-5xl">
            <h2 className="text-3xl font-semibold text-blue-600 mb-6 text-center">
              Analysis Summary
            </h2>

            {/* Emoji Overview */}
            <div className="text-lg mb-8">
              <p><strong>Total Emojis:</strong> {result["Total Emojis"]}</p>
              <p><strong>Overall Sentiment:</strong> {result["Overal Emoji Sentiment"]}</p>
            </div>

            {/* Classified Sentences Table */}
            <div className="mb-6">
              <h3 className="text-xl font-bold text-blue-700 mb-4">
                Classified Sentences
              </h3>
              <table className="table-auto w-full border-collapse border border-gray-800 text-lg">
                <thead>
                  <tr>
                    <th className="border-2 border-gray-800 px-4 py-2 text-left">Sentence</th>
                    <th className="border-2 border-gray-800 px-4 py-2 text-left">Type</th>
                  </tr>
                </thead>
                <tbody>
                  {result.classified_results.map((item, index) => (
                    <tr key={index}>
                      <td className="border-2 border-gray-800 px-4 py-2">{item.Sentence}</td>
                      <td className="border-2 border-gray-800 px-4 py-2">{item.Type}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* General Statements Table */}
            <div className="mb-6">
              <h3 className="text-xl font-bold text-blue-700 mb-4">
                General Statements
              </h3>
              <table className="table-auto w-full border-collapse border border-gray-800 text-lg">
                <thead>
                  <tr>
                    <th className="border-2 border-gray-800 px-4 py-2 text-left">Statement</th>
                    <th className="border-2 border-gray-800 px-4 py-2 text-left">Sentiment</th>
                    <th className="border-2 border-gray-800 px-4 py-2 text-left">Recommendation</th>
                  </tr>
                </thead>
                <tbody>
                  {result.general_statements.map((item, index) => (
                    <tr key={index}>
                      <td className="border-2 border-gray-800 px-4 py-2">
                        {item["General Statement"]}
                      </td>
                      <td className="border-2 border-gray-800 px-4 py-2">{item.Sentiment}</td>
                      <td className="border-2 border-gray-800 px-4 py-2">{item.Recommendation}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Financial Insights Table */}
            <div>
              <h3 className="text-xl font-bold text-blue-700 mb-4">
                Financial Insights
              </h3>
              <table className="table-auto w-full border-collapse border border-gray-800 text-lg">
                <thead>
                  <tr>
                    <th className="border-2 border-gray-800 px-4 py-2 text-left">Statement</th>
                    <th className="border-2 border-gray-800 px-4 py-2 text-left">Sentiment</th>
                    <th className="border-2 border-gray-800 px-4 py-2 text-left">Recommendation</th>
                  </tr>
                </thead>
                <tbody>
                  {result.recommendations.map((item, index) => (
                    <tr key={index}>
                      <td className="border-2 border-gray-800 px-4 py-2">
                        {item["Financial Statement"]}
                      </td>
                      <td className="border-2 border-gray-800 px-4 py-2">{item.Sentiment}</td>
                      <td className="border-2 border-gray-800 px-4 py-2">{item.Recommendation}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
