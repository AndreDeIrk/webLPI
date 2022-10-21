import random

if __name__ == '__main__':
    xs = list([str(i) for i in range(1000)])
    ys = []
    for x in xs:
        ys.append(str(random.random() + int(x) / 40))

    print(f"[{', '.join(xs)}]")
    print(f"[{', '.join(ys)}]")