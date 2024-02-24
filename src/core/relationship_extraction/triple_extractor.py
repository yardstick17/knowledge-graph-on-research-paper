import logging

from transformers import pipeline

logger = logging.getLogger(__name__)

triplet_extractor = pipeline(
    "text2text-generation",
    model="Babelscape/rebel-large",
    tokenizer="Babelscape/rebel-large",
)


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
