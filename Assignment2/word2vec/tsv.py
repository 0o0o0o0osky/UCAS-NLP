import gensim
from pathlib import Path

model = gensim.models.Word2Vec.load("model")
words = [word for word in model.wv.key_to_index.keys()]
logdir = Path('./')

metadata_filename = 'metadata.tsv'
lines = ["index\tlabel"]
for i, word in enumerate(words):
    lines.append(f"{i}\t{word}")
logdir.joinpath(metadata_filename).write_text("\n".join(lines), encoding="utf8")

tensor_filename = 'tensor.tsv'
lines = ["\t".join(map(str, model.wv[word])) for word in words]
logdir.joinpath(tensor_filename).write_text("\n".join(lines), encoding="utf8")

