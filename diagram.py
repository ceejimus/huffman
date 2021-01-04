os_lkp = {
    0: 0
}

def get_offset(depth):
    if depth not in os_lkp:
        n = max(os_lkp.keys())
        while n < depth:
            os_lkp[n + 1] = 2 * os_lkp[n] + 1
            n += 1
    return os_lkp[depth]

def get_members(node, depth, offset, tree_depth):
    if node.is_leaf():
    # if not node.left and not node.right:
        return [(node.get_marker(), depth, offset, 'Leaf')]
    os = get_offset(tree_depth - depth)
    left_members = get_members(node.left, depth + 1, offset - os - 1, tree_depth=tree_depth)
    right_members = get_members(node.right, depth + 1, offset + os + 1, tree_depth=tree_depth)
    return [(node.get_marker(), depth, offset, 'Node')] + left_members + right_members
    
def get_tree_depth(node):
    if node.left is None and node.right is None:
        return 0
    return 1 + max([get_tree_depth(node.left), get_tree_depth(node.right)])

def print_diagram_line(markers, middle):
    line = ''
    current = 0
    total = middle * 2 + 1
    for m in markers:
        while current < (middle + m[2]):
            line += ' '
            current += 1
        line += m[0]
        current += 1
    while current < total:
        line += ' '
        current += 1
    return line

def get_tree_diagram(node):
    lines = []
    tree_depth = node.get_tree_depth()
    middle = 0
    for k in range(1, tree_depth+1):
        middle += (1 + get_offset(k))
    members = get_members(node, 0, 0, tree_depth=tree_depth)
    for i in range(tree_depth+1):
        to_print = sorted([m for m in members if m[1] == i],
            key=lambda x: x[2])
        lines.append(print_diagram_line(to_print, middle))
        slash_lines = []
        for j in range(1, 1 + get_offset(tree_depth-i)):
            slashes = []
            for m in to_print:
                if m[3] == 'Leaf':
                    continue
                left_slash = ('/', None, m[2] - j, 'slash')
                right_slash = ('\\', None, m[2] + j, 'slash')
                slashes += [left_slash, right_slash]
            lines.append(print_diagram_line(slashes, middle))
    return '\n'.join([l.replace('\n', '*') for l in lines])
