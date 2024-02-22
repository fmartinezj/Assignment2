#Francisco Martinez 
#CECS 427
#2/6/2024
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

#reads graph if there is one saved locally
def read_graph(file_name):
    G = nx.Graph()
    with open(file_name, 'r') as file:
        for line in file:
            parts = line.strip().split()  # whitespace seperates the individual parts
            if parts:  # as long as line not empty
                source = parts[0]
                targets = parts[1:]
                for target in targets:
                    G.add_edge(source, target)
    return G

#saves randomaly generated graphs to local memory so that it can be used to plot and compute the shortest paths
def save_graph(G, file_name):
    with open(file_name, 'w') as file:
        for source, targets in G.adjacency():
            line = str(source) + ' ' + ' '.join(map(str,targets)) + '\n'
            file.write(line)

#creates a random graph given the number of nodes and constant factor for generation
def create_random_graph(n, c):
    p = (c*np.log(n))/n  #p is the probability that the nodes are connected to each other
    G = nx.erdos_renyi_graph(n, p) #here is where we use the actual erdos reny graph function from nx
    return G

#shows the shortest path from the chosen source node to the target nodes
#also displays it in the graph (select option 5 after computing the shortest path)
def shortest_path(G, source, target):
    #using shortest path function from nx
    shortestPath = nx.shortest_path(G, source=source, target=target)
    print(f"Shortest path from {source} to {target}: {shortestPath}")
    return shortestPath

#displays the graph that is loaded locally, whether the most recent randomly generated or the most recently saved graph
def plot_graph(G, path=None):
    pos = nx.spring_layout(G)  # I am getting the postion using spring_layout functionality
    nx.draw(G, pos, with_labels=True) #draw graph relative to position and include labels
    
    if path: #activates when running shortest path computation so that it displays the red line (i.e. the shortest path)
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2, style='dotted')
    
    plt.show() #display the actual graph

def karate_club_graph():
    G = nx.karate_club_graph()
    print("Node Degree")
    for v in G:
        # print(f"{v:1000} {G.degree(v):1000}")
        print(f"{v:4} {G.degree(v):6}")

    newG = nx.draw_circular(G, with_labels=True)
    plt.show()
    return G

#runs the program with a menu and try-catch cases to prevent program stops
def main():
    G = None  # Initialize G to None to handle cases where G is not yet defined
    path = None  # Initialize path to None

    while True: #standard menu as instructed
        print("\nWelcome to the Main Menu:")
        print("1. Read Graph")
        print("2. Save graph")
        print("3. Create A Graph")
        print("4. Compute Shortest Path")
        print("5. Plot Graph (G)")
        print("6. Exit Program")
        choice = input("Enter Your Choice (1-6): ")

        if choice == '1':
            file_name = input("Enter the filename to read from: ")
            try:
                G = read_graph(file_name)
                print("Graph has been read successfully.")
            except Exception as e:
                print(f"Error reading graph: {e}")

        elif choice == '2':
            if G is None: #must create or read graph before saving or computing shortest path
                print("No graph has been found in memory. Please create or read a graph first.")
                continue
            file_name = input("Enter the filename to save to: ")
            try:
                save_graph(G, file_name)
                print("Graph saved successfully.")
            except Exception as e:
                print(f"Error saving graph: {e}")

        elif choice == '3':
            print("\nWhat kind of graph would you like to create?")
            print("1) Random Graph (with parameters)")
            print("2) Karate Club Graph")
            subchoice = input("Enter Your Choice (1 or 2): ")
            if subchoice == '1':
                n = int(input("Enter the number of nodes (n): "))
                c = float(input("Enter the constant (c): "))
                G = create_random_graph(n, c)
                print("Random graph created successfully.")
            elif subchoice == '2':
                G = karate_club_graph()
                print("Karate Club graph created successfully.")
            else:
                print("Invalid graph choice. Please enter number 1 or 2.")

        elif choice == '4':
            if G is None:
                print("No graph in memory. Please create or read a graph first.")
                continue
            source = input("Enter the source node: ")
            target = input("Enter the target node: ")
            try:
                path = shortest_path(G, source, target)
            except nx.NetworkXNoPath:
                print(f"No path exists between {source} and {target}.")
            except Exception as e:
                print(f"Error computing shortest path: {e}")

        elif choice == '5':
            if G is None: #same as in step 2
                print("No graph has been found in memory. Please create or read a graph first.")
                continue
            plot_graph(G, path)

        elif choice == '6':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
