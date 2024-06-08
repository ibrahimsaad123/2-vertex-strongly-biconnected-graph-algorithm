import networkx as nx
import urllib.request

# خوارزمية Gabow للعثور على المكونات المتصلة بقوة
def gabow_scc(graph):
    index = [0]
    stack = []
    path = []
    indices = {}
    lowlinks = {}
    on_path = set()
    result = []

    def strongconnect(node):
        indices[node] = index[0]
        lowlinks[node] = index[0]
        index[0] += 1
        stack.append(node)
        path.append(node)
        on_path.add(node)

        for neighbor in graph[node]:
            if neighbor not in indices:
                strongconnect(neighbor)
                lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
            elif neighbor in on_path:
                lowlinks[node] = min(lowlinks[node], indices[neighbor])

        if lowlinks[node] == indices[node]:
            connected_component = []
            while True:
                w = path.pop()
                on_path.remove(w)
                connected_component.append(w)
                if w == node:
                    break
            result.append(connected_component)

    for node in graph:
        if node not in indices:
            strongconnect(node)

    return result

# خوارزمية Jens Schmidt للعثور على العقد المفصلية
def jens_schmidt_articulation_points(graph):
    def dfs(node, parent, depth):
        low[node] = depth
        depths[node] = depth
        visited.add(node)
        children = 0

        for neighbor in graph[node]:
            if neighbor == parent:
                continue
            if neighbor not in visited:
                children += 1
                dfs(neighbor, node, depth + 1)
                low[node] = min(low[node], low[neighbor])
                if low[neighbor] >= depths[node] and parent is not None:
                    articulation_points.add(node)
            else:
                low[node] = min(low[node], depths[neighbor])

        if parent is None and children > 1:
            articulation_points.add(node)

    visited = set()
    low = {}
    depths = {}
    articulation_points = set()

    for node in graph:
        if node not in visited:
            dfs(node, None, 0)

    return articulation_points

# تحميل بيانات مثال من SNAP
url = 'https://snap.stanford.edu/data/email-Eu-core.txt.gz'
filename = 'email-Eu-core.txt.gz'
urllib.request.urlretrieve(url, filename)

# تحميل البيان باستخدام NetworkX
G = nx.read_edgelist(filename, create_using=nx.DiGraph(), nodetype=int)

# التحقق من المكونات المتصلة بقوة باستخدام خوارزمية Gabow
scc = gabow_scc(G)
print("Strongly connected components:", scc)

# تحويل البيان إلى غير موجه والتحقق من العقد المفصلية باستخدام خوارزمية Jens Schmidt
G_undirected = G.to_undirected()
articulation_points = jens_schmidt_articulation_points(G_undirected)
print("Articulation points:", articulation_points)

# التحقق من خاصية 2-vertex strongly biconnected
if len(scc) == 1 and not articulation_points:
    print("The graph is 2-vertex strongly biconnected")
else:
    print("The graph is NOT 2-vertex strongly biconnected")
