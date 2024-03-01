import tkinter as tk
import chess

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game")
        self.selected_square = None  # Initialize selected_square attribute

        self.board = chess.Board()

        # Increase canvas size
        canvas_size = 600
        self.canvas = tk.Canvas(root, width=canvas_size, height=canvas_size)
        self.canvas.pack(side=tk.LEFT)

        # Sidebar for displaying moves
        self.moves_listbox = tk.Listbox(root, width=20)
        self.moves_listbox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.draw_board()
        self.draw_pieces()

        self.canvas.bind("<Button-1>", self.square_clicked)
        self.moves_listbox.bind("<<ListboxSelect>>", self.move_selected)

    def draw_board(self):
        square_size = 600 // 8  # Calculate square size based on canvas size
        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(
                    col * square_size, row * square_size, (col + 1) * square_size, (row + 1) * square_size, fill=color
                )

    def draw_pieces(self):
        square_size = 600 // 8  # Calculate square size based on canvas size
        self.piece_images = {}  # Store references to PhotoImage objects
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is not None:
                filename = f"pieces/{'_' if piece.color == chess.WHITE else ''}{piece.symbol().lower()}.png"
                # Open image and resize
                image = tk.PhotoImage(file=filename)
                image = image.subsample(3)  # Adjust the subsample factor as needed for resizing
                self.piece_images[square] = image  # Store reference
                # Place the resized image on canvas
                self.canvas.create_image(
                    chess.square_file(square) * square_size + square_size // 2,
                    600 - (chess.square_rank(square) * square_size + square_size // 2),
                    image=image,
                )

    def square_clicked(self, event):
        square_size = 600 // 8  # Calculate square size based on canvas size
        col = event.x // square_size
        row = 7 - (event.y // square_size)
        square = chess.square(col, row)
        piece = self.board.piece_at(square)
        if self.selected_square is None:
            if piece is not None and piece.color == self.board.turn:
                self.selected_square = square
                self.canvas.create_rectangle(
                    col * square_size,
                    row * square_size,
                    (col + 1) * square_size,
                    (row + 1) * square_size,
                    outline="blue",
                    width=3,
                    tags="selected",
                )
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                tempboard = self.board.fen()
                self.board.push(move)
                self.canvas.delete("selected")
                self.draw_board()
                self.draw_pieces()
                # Add move to the sidebar
                self.moves_listbox.insert(tk.END, chess.Board(tempboard).san(move))
            self.selected_square = None

    def move_selected(self, event):
        selection = self.moves_listbox.curselection()
        if selection:
            index = int(selection[0])
            move = self.moves_listbox.get(index)
            self.board = self.board.from_board(chess.Board().from_fen(self.board.fen()))
            self.board.push_san(move)
            self.draw_board()
            self.draw_pieces()

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChessGUI(root)
    root.mainloop()
