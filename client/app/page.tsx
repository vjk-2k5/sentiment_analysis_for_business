"use client";
import { useState } from "react";
import { Link } from "@nextui-org/link";
import { Snippet } from "@nextui-org/snippet";
import { Code } from "@nextui-org/code";
import { button as buttonStyles } from "@nextui-org/theme";
import { Textarea, Button } from "@nextui-org/react";

import { siteConfig } from "@/config/site";
import { title, subtitle } from "@/components/primitives";
import { GithubIcon } from "@/components/icons";
//import Sentiment from "sentiment";

export default function SentimentAnalyzer() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);

  const analyzeSentiment = () => {
    const sentiment = new Sentiment();
    const analysis = sentiment.analyze(text);
    setResult(analysis);
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

      <div className="flex</p> flex-col gap-3 w-full max-w-xl">
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
            <p>Score: {result.score}</p>
            <p>Comparative: {result.comparative}</p>
            <p>Positive Words: {result.positive.join(", ")}</p>
            <p>Negative Words: {result.negative.join(", ")}</p>
          </div>
        )}
      </div>

    </section>
  );
}