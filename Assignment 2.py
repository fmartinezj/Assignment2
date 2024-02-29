#Francisco Martinez 
#CECS 427
#2/29/2024
#ASSIGNMENT 2
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import dwave_networkx as dnx 

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
def plot_graph(G, path=None, plot_cluster_coeff=False, plot_neighborhood_overlap=False, overlap_threshold = 0.5, max_pixel=1500, min_pixel=500):
    pos = nx.spring_layout(G)  # I am getting the postion using spring_layout functionality
    # nx.draw(G, pos, with_labels=True) #draw graph relative to position and include labels
    
    if plot_cluster_coeff:
        clustering = nx.clustering(G)
        cluster_min = min(clustering.values())
        cluster_max = max(clustering.values())

        # sizes = {v: min_pixel + (max_pixel - min_pixel) * ((cv - cluster_min) / (cluster_max - cluster_min)) for v, cv in clustering.items()}
        # Adjusted computation of sizes to handle division by zero
        sizes = {}
        if cluster_max - cluster_min == 0:  # All clustering coefficients are the same
            uniform_size = min_pixel + (max_pixel - min_pixel) / 2  # Use an average size
            sizes = {v: uniform_size for v in G.nodes()}
        else:
            sizes = {v: min_pixel + (max_pixel - min_pixel) * ((cv - cluster_min) / (cluster_max - cluster_min)) for v, cv in clustering.items()}
        colors = [(cv - cluster_min) / (cluster_max - cluster_min) * 254 for cv in clustering.values()]
    else:
        sizes = [300 for _ in G.nodes()]  # Default size
        colors = 'skyblue'  # Default color

    nx.draw(G, pos, with_labels=True, node_size=[sizes[v] for v in G.nodes()], node_color=colors if plot_cluster_coeff else 'skyblue')

    if path: #activates when running shortest path computation so that it displays the red line (i.e. the shortest path)
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2, style='dotted')

    overlap_edges = []

    # Highlighting edges based on neighborhood overlap (if enabled)
    if plot_neighborhood_overlap:
        # Compute and plot neighborhood overlap for each edge
        for u, v in G.edges():
            neighbors_u = set(G.neighbors(u))
            neighbors_v = set(G.neighbors(v))
            overlap = len(neighbors_u & neighbors_v) / len(neighbors_u | neighbors_v) if len(neighbors_u | neighbors_v) > 0 else 0
            # Here you could decide on a threshold for highlighting or use overlap value directly for edge color/intensity
            if overlap > overlap_threshold:  # Check if overlap exceeds the threshold
                overlap_edges.append((u, v))

        # Highlight edges with significant overlap
        nx.draw_networkx_edges(G, pos, edgelist=overlap_edges, edge_color='orange', width=2)

    plt.show() #display the actual graph

#from the instructions provided
def karate_club_graph():
    G = nx.karate_club_graph()
    print("Node Degree")
    for v in G:
        # print(f"{v:1000} {G.degree(v):1000}")
        print(f"{v:4} {G.degree(v):6}")

    newG = nx.draw_circular(G, with_labels=True)
    plt.show()
    return G

#partitions the graph based on the number of components the user wishes to break it up into
def partition_graph(G, num_components):
    initial_edges = G.number_of_edges()
    initial_comps = nx.number_connected_components(G)  # Corrected variable name typo
    print("Condition check (Should be True to enter loop):", nx.number_connected_components(G) > num_components)
    current_connected_comps = nx.number_connected_components(G)

    while nx.number_connected_components(G) < num_components:
        print("Inside the loop - modifying the graph.")
        betweenness = nx.edge_betweenness_centrality(G)
        if not betweenness:  # Check if betweenness dictionary is empty
            print("No more edges to remove; the graph is fully disconnected.")
            break  # Exit the loop because there are no more edges to remove
        max_betweenness_edge = max(betweenness, key=betweenness.get)
        G.remove_edge(*max_betweenness_edge)
    
    final_edges = G.number_of_edges()
    final_comps = nx.number_connected_components(G)
    print(f"Initial edges: {initial_edges}, Final edges: {final_edges}")
    print(f"Initial comps: {initial_comps}, Final comps: {final_comps}, Requested comps: {num_components}")
    return G


#assigns colors in order to assess homophily 
def homophily(G, p):
# Here colors are assigned randomnly to each node with influence of p
    for node in G.nodes():
        G.nodes[node]['color'] = 'red' if np.random.rand() < p else 'blue'
    
    # Calculate + print the assortativity coefficient
    assortativity = nx.attribute_assortativity_coefficient(G, 'color')
    print(f"Assortativity coefficient: {assortativity}")
    
    return assortativity

#part of the graph balancing
def balance(G, p):
    # Assign signs to each edge
    for u, v in G.edges():
        G[u][v]['sign'] = '+' if np.random.rand() < p else '-'
    
    #TODO NOT DONE

    #print the edge signs for testing
    print("Edge signs:")
    for u, v, data in G.edges(data=True):
        print(f"{u}-{v}: {data['sign']}")
    
    # TODO replace with actual balance check
    return True  # or False based on your balance checking logic



#runs the program with a menu and try-catch cases to prevent program stops
def main():
    G = None  # Initialize G to None to handle cases where G is not yet defined
    path = None  # Initialize path to None
    
    # Initial state of plotting options
    plot_cluster_coeff = False
    plot_neighborhood_overlap = False
    overlap_threshold = 0.5  # Default value, adjust as needed
    p = 0.5 #default p value to initiate datatype

    while True: #standard menu as instructed
        print("\nWelcome to the Main Menu:")
        print("1. Read Graph")
        print("2. Save graph")
        print("3. Create A Graph")
        print("4. Algorithms")
        print("5. Plot Graph (G)")
        print("6. Assign and Validate Values")
        print("7. Exit Program")
        choice = input("Enter Your Choice (1-7): ")

        if choice == '1':
            file_name = input("Enter the filename to read from: ")
            try:
                G = read_graph(file_name)
                print("Graph has been read successfully.")
            except Exception as e:
                print(f"Error reading graph: {e}") #test

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
            print("\nChoose an algorithm to compute: ")
            print("1) Shortest-Path")
            print("2) Partition G")
            subchoice = input("Enter Your Choice (1 or 2): ")
            if subchoice == '1':
                source = input("Enter the source node: ")
                target = input("Enter the target node: ")
                try:
                    path = shortest_path(G, source, target)
                except nx.NetworkXNoPath:
                    print(f"No path exists between {source} and {target}.")
                except Exception as e:
                    print(f"Error computing shortest path: {e}")
            elif subchoice == '2':
                Components = input("Enter the number (int) of components: ")
                numComponents = int(Components)
                
                G = partition_graph(G, numComponents)
                path = None
                # pos = nx.spring_layout(G)  # Layout for the graph
                # nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500, edge_color='black', linewidths=1, font_size=10)
                # plt.show()
                # plot_graph(G, path)
            else:
                print("Invalid graph choice. Please enter number 1 or 2.")

        elif choice == '5':
            if G is None: #same as in step 2
                print("No graph has been found in memory. Please create or read a graph first.")
                continue
            # Submenu for plotting options
            print("\nGraph Plotting Options:")
            print("1) Toggle Cluster Coefficients")
            print("2) Toggle Neighborhood Overlap")
            print("3) Set Neighborhood Overlap Threshold")
            print("4) Shortest Path")
            print("5) Plot Graph")
            
            plot_choice = input("Enter your choice (1-5): ")

            if plot_choice == '1':
                plot_cluster_coeff = not plot_cluster_coeff
                print(f"Plotting Cluster Coefficients {'Enabled' if plot_cluster_coeff else 'Disabled'}")
            elif plot_choice == '2':
                plot_neighborhood_overlap = not plot_neighborhood_overlap
                print(f"Plotting Neighborhood Overlap {'Enabled' if plot_neighborhood_overlap else 'Disabled'}")
            elif plot_choice == '3':
                if plot_neighborhood_overlap:
                    overlap_threshold = float(input("Enter new overlap threshold (0-1): "))
                    print(f"Neighborhood Overlap Threshold set to {overlap_threshold}")
                else:
                    print("Neighborhood Overlap plotting is not enabled. Enable it first.")
            elif subchoice == '4':
                source = input("Enter the source node: ")
                target = input("Enter the target node: ")
                try:
                    path = shortest_path(G, source, target)
                except nx.NetworkXNoPath:
                    print(f"No path exists between {source} and {target}.")
                except Exception as e:
                    print(f"Error computing shortest path: {e}")
            elif plot_choice == '5':
                plot_graph(G, path, plot_cluster_coeff, plot_neighborhood_overlap, overlap_threshold)
            # plot_graph(G, path)

        elif choice == '6':
           # Submenu for assign and validate options
            print("\nAssign and Validate Options:")
            print("1) Homphily")
            print("2) Balanced Graph")
            attribute_choice = input("Enter your choice (1 or 2): ") #user given option to enter their own p value
            if attribute_choice == '1':
                p = input("Enter p value between 0.0-1.0: ")
                try:
                    p = float(p)
                    if 0.0 <= p <= 1.0:
                        homophily(G, p)
                    else:
                        print("p value must be between 0.0 and 1.0.")
                except ValueError:
                    print("Invalid input. Please enter a valid floating-point number for p.")
            elif attribute_choice == '2':
                p = input("Enter p value between 0.0-1.0: ")
                try:
                    p = float(p)
                    if 0.0 <= p <= 1.0:
                        balance(G, p)
                    else:
                        print("p value must be between 0.0 and 1.0.")
                except ValueError:
                    print("Invalid input. Please enter a valid floating-point number for p.")
                    
            else:
                print("Invalid choice. Please enter number 1 or 2")



        elif choice == '7':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
