import os
import random
from IPython.display import Image, display
from langgraph.graph.state import CompiledStateGraph
from dataclasses import dataclass
from langgraph.graph import StateGraph


@dataclass
class NodeStyles:
    default: str = (
        "fill:#45C4B0, fill-opacity:0.3, color:#23260F, stroke:#45C4B0, stroke-width:1px, font-weight:bold, line-height:1.2"  # 기본 색상
    )
    first: str = (
        "fill:#45C4B0, fill-opacity:0.1, color:#23260F, stroke:#45C4B0, stroke-width:1px, font-weight:normal, font-style:italic, stroke-dasharray:2,2"  # 점선 테두리
    )
    last: str = (
        "fill:#45C4B0, fill-opacity:1, color:#000000, stroke:#45C4B0, stroke-width:1px, font-weight:normal, font-style:italic, stroke-dasharray:2,2"  # 점선 테두리
    )


def visualize_graph(graph, xray=False):
    """
    CompiledStateGraph 객체를 시각화하여 표시합니다.

    이 함수는 주어진 그래프 객체가 CompiledStateGraph 인스턴스인 경우
    해당 그래프를 Mermaid 형식의 PNG 이미지로 변환하여 표시합니다.

    Args:
        graph: 시각화할 그래프 객체. CompiledStateGraph 인스턴스여야 합니다.

    Returns:
        None

    Raises:
        Exception: 그래프 시각화 과정에서 오류가 발생한 경우 예외를 출력합니다.
    """
    try:
        # 그래프 시각화
        if isinstance(graph, CompiledStateGraph):
            display(
                Image(
                    graph.get_graph(xray=xray).draw_mermaid_png(
                        background_color="white",
                        node_colors=NodeStyles(),
                    )
                )
            )
    except Exception as e:
        print(f"[ERROR] Visualize Graph Error: {e}")


def generate_random_hash():
    return f"{random.randint(0, 0xffffff):06x}"

## Jun: Mermaid를 사용하여 그래프 시각화
def visualize_graph_mermaid(builder: StateGraph, output_file="mermaid/graph.html"):
    print("Visualizing graph...")
    nodes = []
    edges = []

    # builder.nodes: {노드_이름: 노드_정의_정보,...} 
    # 단순히 노드 이름만 뽑아 그림에 표현
    for node_name in builder.nodes:
        nodes.append(f'{node_name}["{node_name}"]')

    # builder.edges: [(소스노드, 타겟노드), (소스노드, 타겟노드), ...] 형태라고 가정
    for (source_node, target_node) in builder.edges:
        edges.append(f'{source_node} --> {target_node}')

    mermaid_code = "graph TD\n" + "\n".join(nodes + edges)
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
    </head>
    <body>
        <div class="mermaid">
        {mermaid_code}
        </div>
    </body>
    </html>
    """

    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as file:
            file.write(html_content)
        print(f"Graph saved to {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"Failed to save graph: {e}")
        
