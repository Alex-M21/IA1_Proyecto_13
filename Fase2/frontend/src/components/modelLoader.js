import * as tf from "@tensorflow/tfjs";
import * as use from "@tensorflow-models/universal-sentence-encoder";

let model = null;
let embeddings = [];

export const loadModelAndData = async () => {
  if (model && embeddings.length > 0) {
    return { model, embeddings };
  }

  model = await use.load();

  const trainingDataFromFile = await fetch(`/IA1_Proyecto_13/experimento.json`)
    .then((response) => response.json());

  for (const intent of trainingDataFromFile.intents) {
    for (const example of intent.examples) {
      const embedding = await model.embed([example.userText]);
      embeddings.push({
        vector: embedding.arraySync()[0],
        response: example.botResponse,
      });
    }
  }

  return { model, embeddings };
};
