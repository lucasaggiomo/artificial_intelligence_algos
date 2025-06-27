import threading as th
import tkinter as tk
from test.gameFormulations.pokemon.mossa import Mossa
from test.gameFormulations.pokemon.pokemon import (
    Pokemon,
    PokemonAction,
    PokemonPlayerUmano,
    PokemonState,
)
from test.gameFormulations.pokemon.statistiche import Statistica
from tkinter import ttk
from typing import Callable, Literal, Optional

from PIL import Image, ImageTk

ANIMAZIONE_MS = 1


class PokemonDisplayFrame(tk.Frame):
    def __init__(
        self,
        master,
        pokemon: Pokemon,
        side: Literal["left", "right", "top", "bottom"] = "top",
        anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = "center",
        image_path: Optional[str] = None,
        canvas_on_left: bool = True,
        **kwargs,
    ):
        super().__init__(master, **kwargs)

        self.image_path = image_path
        self.image = None

        self.pack(fill=tk.BOTH, expand=True)

        # frame orizzontale interno per canvas + info
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True, side=side, anchor=anchor)

        # canvas per terreno e immagine
        self.canvas = tk.Canvas(self.main_frame, height=120, highlightthickness=0)

        if image_path:
            img = Image.open(image_path).resize((80, 80))
            self.image = ImageTk.PhotoImage(img)
            self.canvas.create_image(75, 50, image=self.image)

        # frame verticale per nome + PS
        self.info_frame = tk.Frame(self.main_frame)
        self.info_frame.pack(padx=10, pady=10, side=side, anchor=anchor)

        self.label_name = tk.Label(self.info_frame, text=pokemon.name, font=("Arial", 14))
        self.label_name.pack(anchor="w", pady=(0, 4))

        self.ps_frame = tk.Frame(self.info_frame)
        self.ps_frame.pack(anchor="w")

        self.ps_bar = ttk.Progressbar(
            self.ps_frame,
            length=200,
            maximum=pokemon.statistiche[Statistica.PUNTI_SALUTE],
        )
        self.ps_bar.pack(side=tk.LEFT)

        self.ps_label = tk.Label(self.ps_frame, text="")
        self.ps_label.pack(side=tk.LEFT, padx=5)

        if canvas_on_left:
            self.canvas.pack(side=tk.LEFT, padx=5)
            self.info_frame.pack(side=tk.RIGHT, padx=5)
        else:
            self.info_frame.pack(side=tk.LEFT, padx=5)
            self.canvas.pack(side=tk.RIGHT, padx=5)

        self.update_display(pokemon)

        # Posizionamento del blocco principale
        self.pack(side=side, anchor=anchor, padx=10, pady=10)

    def update_display(self, pokemon: Pokemon):
        target_ps = pokemon.statistiche[Statistica.PUNTI_SALUTE]
        self.animazione_ps(target_ps, ANIMAZIONE_MS)

    def animazione_ps(self, target_ps: int, millisecondi: int = 20):
        current_ps = int(self.ps_bar["value"])

        if current_ps == target_ps:
            return

        step = -1 if current_ps > target_ps else 1
        new_ps = current_ps + step

        self.ps_bar["value"] = new_ps
        self.ps_label["text"] = f"{new_ps}/{self.ps_bar['maximum']}"

        # crea l'animazione
        self.after(millisecondi, lambda: self.animazione_ps(target_ps, millisecondi))


class PokemonBattleDisplayFrame(tk.Frame):
    def __init__(
        self,
        master,
        pokemon1: Pokemon,
        pokemon2: Pokemon,
        **kwargs,
    ):
        super().__init__(master, **kwargs)

        self.pack(fill=tk.BOTH, expand=True)

        self.display_p1 = PokemonDisplayFrame(
            self,
            pokemon1,
            side=tk.BOTTOM,
            anchor="se",
            image_path="./test/gameFormulations/pokemon/img/pikachu_back.png",
            canvas_on_left=True,
        )
        self.display_p2 = PokemonDisplayFrame(
            self,
            pokemon2,
            side=tk.TOP,
            anchor="nw",
            image_path="./test/gameFormulations/pokemon/img/bulbasaur_front.webp",
            canvas_on_left=False,
        )

    def update_display(self, pokemon1: Pokemon, pokemon2: Pokemon):
        self.display_p1.update_display(pokemon1)
        self.display_p2.update_display(pokemon2)


class MainFrame(tk.Frame):
    def __init__(self, root: tk.Tk, initialState: PokemonState, waitTurnEvent: th.Event):
        super().__init__(root)
        self.root = root
        self.currentState = initialState
        self.waitTurnEvent = waitTurnEvent

        self.pack(fill=tk.BOTH, expand=True)

        self.setup_ui()

    def setup_ui(self):
        # mostra i pokemon
        self.pokemon_battle = PokemonBattleDisplayFrame(
            self, self.currentState.pokemon1, self.currentState.pokemon2, background="grey"
        )
        self.pokemon_battle.pack(side=tk.TOP, anchor="center")

        # frame per le mosse
        self.move_buttons_frame = tk.Frame(self)
        self.move_buttons_frame.pack(fill="x", side=tk.BOTTOM, anchor="center", padx=5, pady=5)

        self.move_buttons: list[tk.Button] = []
        for i in range(4):
            btn = tk.Button(self.move_buttons_frame, text=f"Mossa {i+1}", state=tk.DISABLED)
            btn.grid(row=0, column=i, padx=5)
            self.move_buttons.append(btn)

        # log battaglia
        self.log = tk.Text(self, height=20, state=tk.DISABLED)
        self.log.pack(fill="x", side=tk.BOTTOM, anchor="center", padx=5, pady=10)

        # pulsante per avviare il turno
        self.avvia_turno_button = tk.Button(
            self, text="Avvia turno", command=self.waitTurnEvent.set
        )
        self.avvia_turno_button.pack(side=tk.BOTTOM, anchor="e", padx=5, pady=5)

        self.update_bars()

    def update_bars(self):
        # devo ripassargli i pokemon (perché il cambio di stato in realtà crea un NUOVO oggetto PokemonState
        # in memoria per far funzionare il transitionModel, creando una deep copy dello stato. Quindi
        # i pokemon del nuovo stato sono oggetti diversi in memoria. L'alternativa era quella di
        # creare una funzione che "aggiornasse" lo stato, ma avrebbe complicato di molto il sistema)
        self.pokemon_battle.update_display(
            self.currentState.pokemon1,
            self.currentState.pokemon2,
        )

    def append_log(self, text: str):
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)

    def update_callback(
        self, oldState: PokemonState, action: PokemonAction, newState: PokemonState
    ) -> None:
        # oldState coincide con self.currentState, ma è presente per completezza
        self.run_action(action, newState)

    def run_action(self, action: PokemonAction, newState: PokemonState):
        self.currentState = newState

        self.append_log(f"{action}")

        self.update_bars()

        if self.currentState.pokemon1.isKO():
            self.append_log(f"{self.currentState.pokemon1.name} è KO. La battaglia è finita")
            self.end_battle()
            return
        elif self.currentState.pokemon2.isKO():
            self.append_log(f"{self.currentState.pokemon2.name} è KO. La battaglia è finita")
            self.end_battle()
            return

        self.append_log("-" * 30)

    def show_moves(
        self,
        pokemon: Pokemon,
        on_move_selected_callback: Callable[[Mossa], None],
    ):
        # aggiorna i bottoni con le mosse attuali del Pokémon
        for i, mossa in enumerate(pokemon.mosse):
            self.move_buttons[i]["text"] = mossa.name
            self.move_buttons[i]["state"] = tk.NORMAL
            self.move_buttons[i]["command"] = lambda m=mossa: self.on_move_selected(
                m, on_move_selected_callback
            )

        # disabilita eventuali bottoni extra
        for i in range(len(pokemon.mosse), 4):
            self.move_buttons[i]["text"] = "-"
            self.move_buttons[i]["state"] = tk.DISABLED

    def on_move_selected(
        self,
        mossa,
        callback: Callable[[Mossa], None],
    ):
        # disabilita i bottoni
        for btn in self.move_buttons:
            btn["state"] = tk.DISABLED

        callback(mossa)  # richiama il metodo del player per continuare chooseAction

    def end_battle(self):
        self.avvia_turno_button.configure(state=tk.DISABLED)


class BattleGUI:
    def __init__(self, initialState: PokemonState, waitTurnEvent: th.Event):
        self.waitTurnEvent = waitTurnEvent

        self.root = tk.Tk()
        self.root.title("Pokemon Battle Simulator")
        self.root.geometry("500x800")

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.mainFrame = MainFrame(self.root, initialState, waitTurnEvent)

        if isinstance(initialState.allenatore1, PokemonPlayerUmano):
            initialState.allenatore1.registerMoveCallback(self.mainFrame.show_moves)

        if isinstance(initialState.allenatore2, PokemonPlayerUmano):
            initialState.allenatore2.registerMoveCallback(self.mainFrame.show_moves)

    def runMainLoop(self):
        self.root.mainloop()

    def update_callback(
        self, oldState: PokemonState, action: PokemonAction, newState: PokemonState
    ) -> None:
        return self.mainFrame.update_callback(oldState, action, newState)

    def on_closing(self):
        print("DISTRUGGO...")
        self.root.destroy()  # dealloca e chiude correttamente
