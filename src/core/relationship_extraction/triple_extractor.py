import logging
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from transformers import pipeline

logger = logging.getLogger(__name__)

triplet_extractor = pipeline(
    "text2text-generation",
    model="Babelscape/rebel-large",
    tokenizer="Babelscape/rebel-large",
)


# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("Babelscape/rebel-large")
model = AutoModelForSeq2SeqLM.from_pretrained("Babelscape/rebel-large")
gen_kwargs = {
    "max_length": 256,
    "length_penalty": 0,
    "num_beams": 3,
    "num_return_sequences": 3,
}


def get_triplets_using_transformers(text):
    # Text to extract triplets from
    # text = 'Punta Cana is a resort town in the municipality of Higüey, in La Altagracia Province, the easternmost province of the Dominican Republic.'

    # Tokenizer text
    model_inputs = tokenizer(
        text, max_length=256, padding=True, truncation=True, return_tensors="pt"
    )

    # Generate
    generated_tokens = model.generate(
        model_inputs["input_ids"].to(model.device),
        attention_mask=model_inputs["attention_mask"].to(model.device),
        **gen_kwargs,
    )

    # Extract text
    decoded_preds = tokenizer.batch_decode(generated_tokens, skip_special_tokens=False)

    # Extract triplets
    """
    Prediction triplets sentence 0
    [{'head': 'life expectancy', 'type': 'facet of', 'tail': 'Longevity'}]
    Prediction triplets sentence 1
    [{'head': 'life expectancy of the Swedish population in 1996', 'type': 'instance of', 'tail': 'life expectancy'}]
    Prediction triplets sentence 2
    [{'head': 'average length of life', 'type': 'facet of', 'tail': 'Longevity'}]
    """
    extracted_triplets = []
    for idx, extracted_text in enumerate(decoded_preds):
        logger.info(f"Extracting relations for: {extracted_text}")
        extracted_triplets.extend(_triplets_using_transformers(extracted_text))
    return extracted_triplets


def get_triplets(text):
    extracted_text_list = triplet_extractor.tokenizer.batch_decode(
        [
            triplet_extractor(text, return_tensors=True, return_text=False)[0][
                "generated_token_ids"
            ]
        ]
    )
    extracted_triplets = []
    logger.info(f"Got total extracted_text_list: {len(extracted_text_list)}")
    for extracted_text in extracted_text_list:
        logger.info(f"Extracting relations for: {extracted_text}")
        extracted_triplets.extend(extract_triplets(extracted_text))
    return extracted_triplets


def _triplets_using_transformers(extracted_text):
    triplets = []
    relation, subject, relation, object_ = "", "", "", ""
    extracted_text = extracted_text.strip()
    current = "x"
    raw_text = (
        extracted_text.replace("<s>", "")
        .replace("<pad>", "")
        .replace("</s>", "")
        .split()
    )
    logger.info(f"raw_text: {raw_text}")

    for token in (
        extracted_text.replace("<s>", "")
        .replace("<pad>", "")
        .replace("</s>", "")
        .split()
    ):
        if token == "<triplet>":
            current = "t"
            if relation != "":
                triplets.append(
                    {
                        "head": subject.strip(),
                        "type": relation.strip(),
                        "tail": object_.strip(),
                    }
                )
                relation = ""
            subject = ""
        elif token == "<subj>":
            current = "s"
            if relation != "":
                triplets.append(
                    {
                        "head": subject.strip(),
                        "type": relation.strip(),
                        "tail": object_.strip(),
                    }
                )
            object_ = ""
        elif token == "<obj>":
            current = "o"
            relation = ""
        else:
            if current == "t":
                subject += " " + token
            elif current == "s":
                object_ += " " + token
            elif current == "o":
                relation += " " + token
    if subject != "" and relation != "" and object_ != "":
        logger.info(
            f" <<SELECTED>> subject: {subject} relation: {relation} tail: {object_}"
        )
        triplets.append(
            {"head": subject.strip(), "type": relation.strip(), "tail": object_.strip()}
        )
    else:
        logger.info(
            f" <<SKIPPED>> subject: {subject} relation: {relation} tail: {object_}"
        )
    return triplets


# Function to parse the generated text and extract the triplets
def extract_triplets(extracted_text):
    triplets = []
    relation, subject, relation, object_ = "", "", "", ""
    extracted_text = extracted_text.strip()
    current = "x"
    for token in (
        extracted_text.replace("<s>", "")
        .replace("<pad>", "")
        .replace("</s>", "")
        .split()
    ):
        if token == "<triplet>":
            current = "t"
            if relation != "":
                triplets.append(
                    {
                        "head": subject.strip(),
                        "type": relation.strip(),
                        "tail": object_.strip(),
                    }
                )
                relation = ""
            subject = ""
        elif token == "<subj>":
            current = "s"
            if relation != "":
                triplets.append(
                    {
                        "head": subject.strip(),
                        "type": relation.strip(),
                        "tail": object_.strip(),
                    }
                )
            object_ = ""
        elif token == "<obj>":
            current = "o"
            relation = ""
        else:
            if current == "t":
                subject += " " + token
            elif current == "s":
                object_ += " " + token
            elif current == "o":
                relation += " " + token
    if subject != "" and relation != "" and object_ != "":
        triplets.append(
            {"head": subject.strip(), "type": relation.strip(), "tail": object_.strip()}
        )
    return triplets


if __name__ == "__main__":
    pass
    # # We need to use the tokenizer manually since we need special tokens.
    # extracted_text_list = triplet_extractor.tokenizer.batch_decode(
    #     [
    #         triplet_extractor(
    #             "Punta Cana is a resort town in the municipality of Higuey, in La Altagracia Province, the eastern most province of the Dominican Republic",
    #             return_tensors=True,
    #             return_text=False,
    #         )[0]["generated_token_ids"]
    #     ]
    # )
    #
    # print(extracted_text_list[0])
    # extracted_triplets = extract_triplets(extracted_text_list[0])
    # print(extracted_triplets)
