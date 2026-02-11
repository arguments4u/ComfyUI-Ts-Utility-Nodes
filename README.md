# ComfyUI-Ts-Utility-Nodes

A collection of custom nodes designed to streamline and enhance workflows within ComfyUI.

## Installation

1. Navigate to your `custom_nodes` directory:

```bash
cd ComfyUI/custom_nodes/

```

2. Clone this repository:

```bash
git clone https://github.com/arguments4u/ComfyUI-Ts-Utility-Nodes.git

```

3. Install the required dependencies:

```bash
pip install -r requirements.txt

```

## Nodes

### Load Image RGB (Clip Snapshot) / Load Image RGBA (Clip Snapshot)

These nodes allow you to load images from the clipboard by **capturing a snapshot at the exact moment of queueing**.
This ensures that the correct data is processed even if your clipboard is overwritten before the actual node execution.

* **Load Image RGB (Clip Snapshot):** Processes images in RGB mode.
* **Load Image RGBA (Clip Snapshot):** Processes images in RGBA mode (with alpha channel).

The nodes also support clipboard data that contains direct **file paths** or **URLs** to image files.

#### Input/Output

* Load Image RGB (Clip Snapshot)
    * Inputs:
        * default_image (IMAGE): the default image output when clipboard data cannot be imported as an image
    * Outputs:
        * image (IMAGE): the image loaded from snapshot
        * filepath (STRING): path to the snapshot
* Load Image RGBA (Clip Snapshot)
    * Inputs:
        * default_image (IMAGE): the default image output when clipboard data cannot be imported as an image
    * Outputs:
        * image (IMAGE): the image loaded from color channel of snapshot
        * mask (MASK): the mask loaded from alpha channel of snapshot
        * filepath (STRING): path to the snapshot

#### Key Features

Upon queueing, the node resolves the clipboard content into a local file path and writes it to a specific entry in `extra_pnginfo`*:
**Path: `extra_pnginfo['extra_data']['extra_pnginfo']['ts_utility_nodes']['path_to_input_image']*`

* **Raw Image Data:** Saves the image to the `input/pasted` folder and retrieves its path.
* **URL:** Downloads the image from the specified URL to the `input/pasted` folder and retrieves its path.
* **File Path:** Uses the existing file path directly.

#### Specifications

* **Storage Location:** `ComfyUI/input/pasted` (Consistent with the standard ComfyUI `Ctrl+V` feature).
* **Naming Convention:** `image_%Y-%m-%d_%H-%M-%S.png` (e.g., `image_2024-03-21_15-30-45.png`).
* **Metadata & Reproducibility:** Since the resolved path is stored within `extra_pnginfo`, the workflow remains fully reproducible even if the clipboard changes later.

---

ComfyUIで自分の作業を効率化するために作成しているカスタムノード群です。

## インストール

1. `custom_nodes` フォルダに移動します。
```bash
cd ComfyUI/custom_nodes/

```


2. このリポジトリをクローンします。
```bash
git clone https://github.com/arguments4u/ComfyUI-LoadImage-ClipSnapshot.git

```


3. 依存ライブラリをインストールします。
```bash
pip install -r requirements.txt

```

## ノード

### Load Image RGB (Clip Snapshot) / Load Image RGBA (Clip Snapshot)

クリップボードの内容を**キューイング時に確定（スナップショット）**して読み込むためのカスタムノードです。
ノードの実行までにクリップボードが上書きされても問題なく動作します。
"Load Image RGB (Clip Snapshot)"はRGB画像、"Load Image RGBA (Clip Snapshot)"はRGBA画像を読み込みます。

また、クリップボード上のデータが画像ファイルへのファイルパスまたはURLである場合にも対応しています。

#### 入出力

* Load Image RGB (Clip Snapshot)
    * Inputs:
        * default_image (IMAGE): the default image output when clipboard data cannot be imported as an image
    * Outputs:
        * image (IMAGE): the image loaded from snapshot
        * filepath (STRING): path to the snapshot
* Load Image RGBA (Clip Snapshot)
    * Inputs:
        * default_image (IMAGE): the default image output when clipboard data cannot be imported as an image
    * Outputs:
        * image (IMAGE): the image loaded from color channel of snapshot
        * mask (MASK): the mask loaded from alpha channel of snapshot
        * filepath (STRING): path to the snapshot

#### 主な機能

クリップボードの中身に応じて、キューイング時に以下の通りパスの取得を行い、取得したパスをextra_pnginfoの所定のパス※に書き込みます。<br>
※extra_pnginfo['extra_data']['extra_pnginfo']['ts_utility_nodes']['path_to_input_image']

* **画像データ:** `input/pasted` フォルダに画像データを保存し、そのパスを取得
* **URL:** 指定されたURLから画像を `input/pasted` にダウンロードし、そのパスを取得。
* **ファイルパス:** そのパスをそのまま取得。

#### 仕様

* **保存先:** `ComfyUI/input/pasted` (標準のCtrl+V機能と共通)
* **ファイル命名規則:** `image_%Y-%m-%d_%H-%M-%S.png` (例: `image_2024-03-21_15-30-45.png`)
* **メタデータ:** 生成されたパス情報は `extra_pnginfo` に保存されるため、ワークフローの再現性が保証されます。
