import tkinter
from system import BookingSystem


def main():
    
    # inciamos a parte visual da interface com o tkinter
    # Cria a janela do tkinter
    root = tkinter.Tk()
    root.title("Forex Dechathlon") #demos um titulo à janela
    
    # Damos inicio ao nosso programa
    print("Programa a inciar...")
    sistema = BookingSystem()

    
    root.mainloop() 
    
    # a interface só apareco quando eu quero que corra
    # e não quando testo partes de código individualmente
    if __name__ == "__main__":
        main()
