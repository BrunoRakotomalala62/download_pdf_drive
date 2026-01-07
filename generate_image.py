import matplotlib.pyplot as plt

def generate_math_image():
    # Content with simple LaTeX-style notation supported by Matplotlib's mathtext
    content = [
        (r"$\mathbf{CORRECTION\ DE\ L'EXERCICE}$", 'blue', 20, 'center'),
        ("", 'black', 10, 'left'),
        (r"$\mathbf{1)\ a.\ Montrons\ par\ récurrence\ que\ } U_n < 6 :$", 'red', 14, 'left'),
        (r"$\bullet\ \mathrm{Initialisation\ :\ Pour\ } n=0, U_0 = 2. \mathrm{\ Comme\ } 2 < 6, \mathrm{\ c'est\ vrai.}$", 'black', 12, 'left'),
        (r"$\bullet\ \mathrm{Hérédité\ :\ Supposons\ que\ pour\ un\ entier\ } n \mathrm{\ donné,\ } U_n < 6.$", 'black', 12, 'left'),
        (r"$\quad \frac{1}{2}U_n < 3 \rightarrow \frac{1}{2}U_n + 3 < 6 \rightarrow U_{n+1} < 6.$", 'black', 12, 'left'),
        (r"$\bullet\ \mathrm{Conclusion\ :\ Pour\ tout\ } n, U_n < 6.$", 'black', 12, 'left'),
        ("", 'black', 10, 'left'),
        (r"$\mathbf{1)\ b.\ Calcul\ de\ } U_{n+1} - U_n \mathbf{\ et\ monotonie\ :}$", 'red', 14, 'left'),
        (r"$U_{n+1} - U_n = (\frac{1}{2}U_n + 3) - U_n = -\frac{1}{2}U_n + 3$", 'black', 12, 'left'),
        (r"$\quad = \frac{6 - U_n}{2}$", 'black', 12, 'left'),
        (r"$\mathrm{Or,\ } U_n < 6 \rightarrow 6 - U_n > 0. \mathrm{\ Le\ résultat\ est\ positif.}$", 'black', 12, 'left'),
        (r"$\mathrm{Donc\ } (U_n) \mathrm{\ est\ strictement\ croissante.}$", 'black', 12, 'left'),
        ("", 'black', 10, 'left'),
        (r"$\mathbf{1)\ c.\ Convergence\ :}$", 'red', 14, 'left'),
        (r"$(U_n) \mathrm{\ est\ croissante\ et\ majorée\ par\ 6.\ Donc\ } (U_n) \mathrm{\ est\ convergente.}$", 'black', 12, 'left'),
        ("", 'black', 15, 'left'),
        (r"$\mathbf{2)\ On\ pose\ } V_n = U_n - 6.$", 'blue', 14, 'left'),
        ("", 'black', 5, 'left'),
        (r"$\mathbf{2)\ a.\ Nature\ de\ la\ suite\ } (V_n) :$", 'red', 14, 'left'),
        (r"$V_{n+1} = U_{n+1} - 6 = (\frac{1}{2}U_n + 3) - 6 = \frac{1}{2}U_n - 3$", 'black', 12, 'left'),
        (r"$V_{n+1} = \frac{1}{2}(U_n - 6) = \frac{1}{2}V_n$", 'black', 12, 'left'),
        (r"$\mathrm{C'est\ une\ suite\ géométrique\ de\ raison\ } q = \frac{1}{2}.$", 'black', 12, 'left'),
        ("", 'black', 10, 'left'),
        (r"$\mathbf{2)\ b.\ Expression\ de\ } V_n \mathbf{\ et\ } U_n :$", 'red', 14, 'left'),
        (r"$\mathrm{Premier\ terme\ :\ } V_0 = U_0 - 6 = 2 - 6 = -4.$", 'black', 12, 'left'),
        (r"$\mathrm{Terme\ général\ :\ } V_n = V_0 \times q^n = -4 \times (\frac{1}{2})^n.$", 'black', 12, 'left'),
        (r"$\mathrm{Comme\ } V_n = U_n - 6, \mathrm{\ alors\ } U_n = V_n + 6.$", 'black', 12, 'left'),
        (r"$U_n = 6 - 4 \times (\frac{1}{2})^n.$", 'black', 12, 'left'),
        ("", 'black', 10, 'left'),
        (r"$\mathbf{2)\ c.\ Limite\ de\ } U_n :$", 'red', 14, 'left'),
        (r"$\mathrm{On\ sait\ que\ } -1 < \frac{1}{2} < 1, \mathrm{\ donc\ } \lim_{n \rightarrow \infty} (\frac{1}{2})^n = 0.$", 'black', 12, 'left'),
        (r"$\lim_{n \rightarrow \infty} U_n = 6 - 4 \times 0 = 6.$", 'black', 12, 'left'),
        (r"$\mathbf{\lim_{n \rightarrow \infty} U_n = 6}$", 'blue', 16, 'center'),
    ]

    fig, ax = plt.subplots(figsize=(8, 11))
    ax.axis('off')
    
    y_pos = 0.95
    for text, color, size, align in content:
        if text == "":
            y_pos -= size / 1000
            continue
            
        x_pos = 0.5 if align == 'center' else 0.05
        ax.text(x_pos, y_pos, text, color=color, fontsize=size, 
                ha=align, va='top', transform=ax.transAxes)
        y_pos -= (size + 15) / 1000

    plt.savefig("correction_exercice_suites.jpg", dpi=200, bbox_inches='tight')
    plt.close()
    print("L'image avec rendu mathématique a été générée : correction_exercice_suites.jpg")

if __name__ == "__main__":
    generate_math_image()
