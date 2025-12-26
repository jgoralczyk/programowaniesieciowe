# words = ["cat", "mountain", "sun", "python", "ai"]

# upperlonger = [w.upper() for w in words if len(w)> 3]

# print(upperlonger)


# words = ['mountain', 'python']
# lengths = [len(w) for w in words]

# for i, (w, l) in enumerate(zip(words, lengths)):
#     print(f"{i}: {w.upper()} ({l}) ")
    
    
names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
scores = [85, 42, 91, 68, 100]
passed = [True, False, True, True, True]


#exampassed = [(i, name, score, p) for i, (name, score, p) in enumerate(zip(names,scores,passed)) if p]

result = [
    f"{i}. {name.upper()} – {score} {'✅' if score > 70 else '❌'}"
    for i, (name, score, p) in enumerate(zip(names, scores, passed))
    if p
]
print(result)


