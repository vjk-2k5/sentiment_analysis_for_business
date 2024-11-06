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
        <h1 className={title({ color: "green" })}>Sentiment Analyzer for Business &nbsp;</h1>
        <br />
        <div className={subtitle({ class: "mt-4" })}>
          Simply enter the text you want to analyze in the textarea below and click on the "Analyze" button.
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
        <Button
          className="mt-4"
          onClick={analyzeSentiment}
          color="primary"
          auto
        >
          Analyze
        </Button>
        {result && (
          <div className="mt-4 text-center">
            <h2 className="text-xl font-semibold">Analysis Result</h2>
            <p>Total Emojis: {result["Total Emojis"]}</p>
            <p>Overall Sentiment: {result["Overal Emoji Sentiment"]}</p>
            <div>
              <h3 className="text-lg font-semibold">Classified Results</h3>
              {result.classified_results.map((item, index) => (
                <div key={index}>
                  <p>Sentence: {item.Sentence}</p>
                  <p>Type: {item.Type}</p>
                </div>
              ))}
            </div>
            <div>
              <h3 className="text-lg font-semibold">General Statements</h3>
              {result.general_statements.map((item, index) => (
                <div key={index}>
                  <p>General Statement: {item["General Statement"]}</p>
                  <p>Sentiment: {item.Sentiment}</p>
                  <p>Recommendation: {item.Recommendation}</p>
                </div>
              ))}
            </div>
            <div>
              <h3 className="text-lg font-semibold">Recommendations</h3>
              {result.recommendations.map((item, index) => (
                <div key={index}>
                  <p>Financial Statement: {item["Financial Statement"]}</p>
                  <p>Recommendation: {item.Recommendation}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}