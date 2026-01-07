import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from IPython.display import HTML, display
import numpy as np

def _apply_colormap(relevance, cmap):
    colormap = cm.get_cmap(cmap)
    return colormap(colors.Normalize(vmin=-1, vmax=1)(relevance))

def jupyter_heatmap(tokens, relevances, cmap="bwr"):
    """
    Display a heatmap of token relevances in a Jupyter notebook using HTML.
    
    Parameters
    ----------
    tokens : list of str
        The tokens in the sentence.
    relevances : list of float or numpy array
        The relevances of the tokens normalized between -1 and 1.
    cmap : str
        The name of the colormap to use (default: 'bwr' - blue-white-red).
    
    Returns
    -------
    IPython.display.HTML
        An HTML object that will be rendered in the notebook.
    """
    assert len(tokens) == len(relevances), "The number of tokens and relevances must be the same."
    
    # Convert to list if numpy array
    if hasattr(relevances, 'min'):
        assert relevances.min() >= -1 and relevances.max() <= 1, \
            "The relevances must be normalized between -1 and 1."
    
    html_parts = ['<div style="line-height: 1.8; font-size: 16px; font-family: Arial, sans-serif; padding: 10px; border: 2px solid #333;">']
    
    for token, relevance in zip(tokens, relevances):
        rgb = _apply_colormap(relevance, cmap)
        r, g, b = int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)
        
        # Determine text color for better readability
        # Use white text on dark backgrounds, black on light
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        text_color = 'white' if luminance < 0.5 else 'black'
        
        html_parts.append(
            f'<span style="background-color: rgb({r},{g},{b}); '
            f'color: {text_color}; padding: 2px 4px; margin: 1px; '
            f'display: inline-block; border-radius: 2px;">{token}</span>'
        )
    
    html_parts.append('</div>')
    
    html_content = ''.join(html_parts)
    return display(HTML(html_content))

def decode_tokens_for_plotting(input_ids, tokenizer):
    """
    Convert input IDs to cleaned tokens for plotting.
    """

    tokens = [tokenizer.decode([idx]) for idx in input_ids]
    special_characters = ['&', '%', '$', '#', '_', '{', '}', '\\']
    for i, t in enumerate(tokens):
        for special_character in special_characters:
            if special_character in t:
                tokens[i] = t.replace(special_character, '\\' + special_character)
    return tokens

def plot_atlas(
    df,
    color_col='cluster',
    size_col='score',
    top_k=None,
    scale_factor=1000,
    figsize=(6, 5),
    cmap_name='tab10'
):
    """
    Plots a bubble chart of Head vs Layer specialization.

    If top_k is provided and color_col is categorical, it filters the top_k
    items PER CATEGORY. Otherwise, it filters the top_k items GLOBALLY.
    """

    # 1. Determine Color Mode
    is_categorical = False
    if df[color_col].dtype == 'object' or df[color_col].dtype.name == 'category':
        is_categorical = True
    elif df[color_col].nunique() < 20:
        is_categorical = True

    # 2. Filter Data (Top K)
    df_plot = df.copy()
    df_plot['abs_score_temp'] = df_plot[size_col].abs()

    if top_k is not None:
        if is_categorical:
            # Filter Top K per Category
            df_plot = df_plot.groupby(color_col, group_keys=False).apply(
                lambda x: x.nlargest(top_k, 'abs_score_temp')
            )
            title_suffix = f"(Top {top_k} per {color_col})"
        else:
            # Filter Top K Globally (since there are no categories)
            df_plot = df_plot.nlargest(top_k, 'abs_score_temp')
            title_suffix = f"(Top {top_k} Global)"
    else:
        title_suffix = " "

    # 3. Prepare Plot Arrays
    x_plot = df_plot['head']
    y_plot = df_plot['layer']
    sizes_plot = df_plot['abs_score_temp'] * scale_factor

    # 4. Setup Plot
    plt.figure(figsize=figsize)
    plt.grid(True, linestyle='--', alpha=0.3)

    if is_categorical:
        # Categorical Logic
        unique_vals = sorted(df_plot[color_col].unique())
        cmap = plt.get_cmap(cmap_name)

        val_to_color = {
            val: cmap(i % cmap.N) for i, val in enumerate(unique_vals)
        }
        colors_plot = df_plot[color_col].map(val_to_color)

        plt.scatter(
            x_plot, y_plot, s=sizes_plot, c=colors_plot,
            alpha=0.6, edgecolors='none'
        )

        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label=f'{val}',
                   markerfacecolor=color, markersize=10)
            for val, color in val_to_color.items()
        ]
        plt.legend(handles=legend_elements, loc='upper right', title=color_col.capitalize())

    else:
        # Continuous Logic
        scatter = plt.scatter(
            x_plot, y_plot, s=sizes_plot, c=df_plot[color_col],
            cmap='viridis', alpha=0.6, edgecolors='none'
        )
        cbar = plt.colorbar(scatter)
        cbar.set_label(color_col.capitalize(), rotation=270, labelpad=15)

    # 5. Formatting
    plt.gca().invert_yaxis()

    plt.title(f"Head Specialization {title_suffix}", fontsize=16)
    plt.xlabel("Head ID", fontsize=14)
    plt.ylabel("Layer ID", fontsize=14)

    if not df.empty:
        plt.xticks(np.arange(0, df['head'].max() + 1, 2))
        plt.yticks(np.arange(0, df['layer'].max() + 1, 1))

    plt.tight_layout()
    plt.show()


