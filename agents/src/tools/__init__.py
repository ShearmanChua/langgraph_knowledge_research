"""
LangGraph Research Agent Tools

This module provides a collection of tools for research agents, including:
- Web search and scraping (DuckDuckGo, Playwright)
- ArXiv paper search and PDF reading
- Note-taking with Markdown sections
- Elasticsearch queries
- PostgreSQL database access
- Weaviate vector database operations
- Graph management with Mermaid export
"""

from .tracing import trace_tool, trace_sync_tool

from .web_tools import (
    search_web,
    open_webpage,
    next_search_page,
    get_web_tools,
)

from .arxiv_tools import (
    search_arxiv,
    get_paper_abstract,
    open_paper,
    search_paper_keyword,
    next_paper_window,
    prev_paper_window,
    read_paper_window,
    next_arxiv_page,
    get_arxiv_tools,
)

from .note_tools import (
    create_note_section,
    create_note_subsection,
    write_notes,
    edit_note_section,
    delete_note_section,
    list_note_sections,
    read_note_section,
    read_all_notes,
    get_note_tools,
)

from .es_tools import (
    init_elasticsearch,
    list_es_indices,
    get_es_index_mapping,
    view_es_documents,
    run_es_query,
    get_es_tools,
)

from .sql_tools import (
    init_postgres,
    list_sql_tables,
    describe_sql_table,
    preview_sql_table,
    filter_sql_table,
    run_sql_query,
    get_sql_tools,
)

from .weaviate_tools import (
    init_weaviate,
    list_weaviate_classes,
    get_weaviate_class_schema,
    view_weaviate_objects,
    filter_weaviate_objects,
    hybrid_search_weaviate,
    get_weaviate_tools,
)

from .graph_tools import (
    create_graph,
    list_graphs,
    add_graph_node,
    get_graph_node,
    update_graph_node,
    add_graph_edge,
    get_graph_edge,
    update_graph_edge,
    get_graph_mermaid,
    get_graph_tools,
)


def get_all_tools():
    """
    Return all available tools for the research agent.
    
    Returns:
        List of all tool functions.
    """
    return (
        get_web_tools() +
        get_arxiv_tools() +
        get_note_tools() +
        get_es_tools() +
        get_sql_tools() +
        get_weaviate_tools() +
        get_graph_tools()
    )


def get_research_tools():
    """
    Return core research tools (web, arxiv, notes).
    
    Returns:
        List of research-focused tool functions.
    """
    return (
        get_web_tools() +
        get_arxiv_tools() +
        get_note_tools()
    )


def get_data_tools():
    """
    Return data access tools (ES, SQL, Weaviate).
    
    Returns:
        List of data access tool functions.
    """
    return (
        get_es_tools() +
        get_sql_tools() +
        get_weaviate_tools()
    )


__all__ = [
    # Tracing
    "trace_tool",
    "trace_sync_tool",
    
    # Web tools
    "search_web",
    "open_webpage",
    "next_search_page",
    "get_web_tools",
    
    # ArXiv tools
    "search_arxiv",
    "get_paper_abstract",
    "open_paper",
    "search_paper_keyword",
    "next_paper_window",
    "prev_paper_window",
    "read_paper_window",
    "next_arxiv_page",
    "get_arxiv_tools",
    
    # Note tools
    "create_note_section",
    "create_note_subsection",
    "write_notes",
    "edit_note_section",
    "delete_note_section",
    "list_note_sections",
    "read_note_section",
    "read_all_notes",
    "get_note_tools",
    
    # Elasticsearch tools
    "init_elasticsearch",
    "list_es_indices",
    "get_es_index_mapping",
    "view_es_documents",
    "run_es_query",
    "get_es_tools",
    
    # SQL tools
    "init_postgres",
    "list_sql_tables",
    "describe_sql_table",
    "preview_sql_table",
    "filter_sql_table",
    "run_sql_query",
    "get_sql_tools",
    
    # Weaviate tools
    "init_weaviate",
    "list_weaviate_classes",
    "get_weaviate_class_schema",
    "view_weaviate_objects",
    "filter_weaviate_objects",
    "hybrid_search_weaviate",
    "get_weaviate_tools",
    
    # Graph tools
    "create_graph",
    "list_graphs",
    "add_graph_node",
    "get_graph_node",
    "update_graph_node",
    "add_graph_edge",
    "get_graph_edge",
    "update_graph_edge",
    "get_graph_mermaid",
    "get_graph_tools",
    
    # Aggregated tool getters
    "get_all_tools",
    "get_research_tools",
    "get_data_tools",
]
