# ComfyUI MiniMax H3 Conditioning Saver & Loader

Custom nodes for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) that let you save MiniMax H3 reference-conditioned outputs to disk and reload them in subsequent workflows.

The extension is designed for workflows using the **MiniMax H3 Reference to Video** node, including prompts conditioned on reference images, videos, and audio.

## Features

- **Save conditioning:** Serialize ComfyUI `CONDITIONING` data to a PyTorch `.pt` file.
- **Load conditioning:** Restore saved conditioning data for reuse in another workflow or session.
- **Preserve reference metadata:** Retain the conditioning structure, including MiniMax H3 reference data such as `minimax_refs`.
- **Workflow integration:** Connect the nodes to existing ComfyUI conditioning pipelines.
- **Output-node execution:** The saver is an output node, allowing ComfyUI to execute it through the normal Run workflow.
- **Configurable filenames:** Specify a filename for each saved conditioning file.

## Nodes

### 1. MiniMax H3 Conditioning Saver

Saves a conditioning object received from another node to a `.pt` file.

**Inputs**

| Input | Type | Description |
|---|---|---|
| `conditioning` | CONDITIONING | Conditioning data to save |
| `filename` | STRING | Name of the output file |

**Output directory**

```text
ComfyUI/output/minimax_h3_conditioning/
```

Example:

```text
ComfyUI/output/minimax_h3_conditioning/cond_scene_01.pt
```

The saver operates as an output node and does not require a downstream connection.

### 2. MiniMax H3 Conditioning Loader

Loads a previously saved conditioning file and exposes it as a `CONDITIONING` output.

**Inputs**

| Input | Type | Description |
|---|---|---|
| `filename` | STRING | Name of the saved `.pt` file |

**Output**

| Output | Type | Description |
|---|---|---|
| `conditioning` | CONDITIONING | Restored conditioning data |

The loader reads files from the extension's conditioning output directory.

## Installation

### Manual installation

1. Navigate to your ComfyUI `custom_nodes` directory.
2. Clone this repository:

   ```bash
   git clone https://github.com/YOUR_USERNAME/ComfyUI-MiniMaxH3ConditioningSaver.git
   ```

3. Restart ComfyUI.
4. Search for the following nodes in the node menu:
   - `MiniMax H3 Conditioning Saver`
   - `MiniMax H3 Conditioning Loader`

Replace `YOUR_USERNAME` with your GitHub username and adjust the repository URL if you choose a different name.

### Dependencies

The nodes use PyTorch and ComfyUI's existing Python environment. They do not require a separate model download.

## Usage

### Saving conditioning

1. Add the **MiniMax H3 Reference to Video** node to your workflow.
2. Configure the prompt, reference images, videos, audio, and other required inputs.
3. Connect the node's `positive` conditioning output to the `conditioning` input of **MiniMax H3 Conditioning Saver**.
4. Enter a filename, for example:

   ```text
   cond_scene_01.pt
   ```

5. Execute the workflow using ComfyUI's Run button.

The conditioning data is saved under:

```text
ComfyUI/output/minimax_h3_conditioning/cond_scene_01.pt
```

### Loading conditioning

1. Add **MiniMax H3 Conditioning Loader** to a workflow.
2. Enter the filename of a previously saved conditioning file.
3. Connect its `conditioning` output to a compatible downstream node.
4. Execute the workflow.

This allows you to reuse saved conditioning without necessarily rerunning the original reference-conditioning node.

## Important considerations

### Conditioning is not a video

These nodes save and restore conditioning data. They do not save the generated video, model weights, or the complete workflow configuration.

### Reference data and storage

MiniMax H3 conditioning can contain tensors and metadata associated with reference images, video latents, and audio latents. File sizes depend on the reference data and conditioning structure.

### Compatibility

Saved files are intended for compatible ComfyUI and MiniMax H3 environments. Changes to the node implementation, model architecture, conditioning format, or tensor layout may affect compatibility.

The loader restores the serialized object; it does not independently recreate missing reference data or convert incompatible conditioning formats.

### Security

Files are serialized using PyTorch. Loading `.pt` files with unrestricted pickle deserialization can execute malicious code. **Only load files from trusted sources.** Do not load arbitrary conditioning files downloaded from the internet.

### Backup

Saved files are stored in ComfyUI's output directory. Back up important conditioning files if they are needed for future workflows.

## Troubleshooting

**Node not visible after installation**
- Restart ComfyUI completely.
- Check the startup console for Python import or syntax errors.
- Verify that the extension is installed under `ComfyUI/custom_nodes/`.

**Conditioning file not found**
- Confirm that the filename matches the saved file.
- Verify that the file exists under `output/minimax_h3_conditioning/`.
- Ensure that the saver and loader use the same output directory.

**Errors during video generation**
- Verify that the downstream node accepts the restored `CONDITIONING` structure.
- Check compatibility with your MiniMax H3 implementation.
- Confirm that reference latents and tensors are handled correctly by the target device and sampler.

## Acknowledgements

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- MiniMax H3 reference-to-video conditioning and the associated ComfyUI implementation.
