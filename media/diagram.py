# class_diagram_memory.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

def draw_class(ax, x, y, w, h, name, attrs, methods, color='lightblue'):
    # Caja redondeada
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2",
                          edgecolor='black', facecolor=color, linewidth=2)
    ax.add_patch(rect)
    # Nombre de la clase
    ax.text(x + w/2, y + h - 8, name, ha='center', va='top',
            fontsize=14, fontweight='bold')
    # Línea divisoria
    ax.plot([x+2, x+w-2], [y + h - 22, y + h - 22], color='black', lw=1.5)
    # Atributos
    y_attr = y + h - 36
    for a in attrs:
        ax.text(x + 6, y_attr, a, fontsize=11, va='top')
        y_attr -= 18
    # Línea divisoria de métodos
    ax.plot([x+2, x+w-2], [y_attr + 10, y_attr + 10], color='black', lw=1.5)
    # Métodos
    y_meth = y_attr - 4
    for m in methods:
        ax.text(x + 6, y_meth, m, fontsize=11, va='top')
        y_meth -= 18
    return rect

def draw_arrow(ax, start, end, label='', label_pos='mid'):
    arrow = FancyArrowPatch(start, end, arrowstyle='->', mutation_scale=20,
                            color='black', lw=2)
    ax.add_patch(arrow)
    if label:
        if label_pos == 'mid':
            mx = (start[0] + end[0]) / 2
            my = (start[1] + end[1]) / 2
            ax.text(mx, my + 5, label, ha='center', fontsize=11, color='darkred')
        elif label_pos == 'top':
            ax.text(end[0], end[1] + 5, label, ha='center', fontsize=11, color='darkred')
        elif label_pos == 'bottom':
            ax.text(end[0], end[1] - 5, label, ha='center', fontsize=11, color='darkred')

fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

# Clase Card (izquierda)
draw_class(ax, 0.5, 5.0, 3.0, 2.6, 'Card',
           ['- pair_id: int', '- face_up: bool', '- matched: bool',
            '- image: Surface', '- rect: Rect'],
           ['+ draw(surface, x, y)', '+ flip()', '+ set_matched()'])

# Clase Board (centro-izquierda)
draw_class(ax, 4.5, 5.0, 3.2, 3.0, 'Board',
           ['- rows: int', '- cols: int', '- theme: str', '- cards: list[list[Card]]'],
           ['+ generate_board()', '+ get_card(row, col)', '+ all_matched()',
            '+ reset()', '+ load_images_for_theme()'])

# Clase Player (centro-derecha)
draw_class(ax, 9.0, 5.0, 2.8, 2.2, 'Player',
           ['- name: str', '- is_human: bool', '- score: int'],
           ['+ add_pair()'])

# Clase Game (abajo)
draw_class(ax, 4.5, 0.5, 3.8, 3.2, 'Game',
           ['- screen: Surface', '- clock: Clock', '- running: bool',
            '- board: Board', '- players: list[Player]',
            '- current_player: int', '- selected_cards: list',
            '- waiting: bool', '- wait_timer: int', '- theme: str'],
           ['+ run()', '+ handle_events()', '+ handle_click(pos)',
            '+ update()', '+ check_pair()', '+ ai_turn()',
            '+ next_turn()', '+ render()', '+ end_game()'])

# Relaciones
# Game -> Board (composición, 1 a 1)
draw_arrow(ax, (6.4, 3.7), (6.1, 4.8), label='1')
# Game -> Player (composición, 1 a *)
draw_arrow(ax, (7.0, 3.7), (8.5, 4.8), label='1..*')
# Board -> Card (composición, contiene múltiples cartas)
draw_arrow(ax, (4.5, 5.0), (3.5, 5.0), label='rows*cols')

plt.title('Diagrama de clases - Memory Venezuela', fontsize=18, fontweight='bold')
plt.tight_layout()
plt.savefig('class_diagram_memory.png', dpi=300, bbox_inches='tight')
plt.show()