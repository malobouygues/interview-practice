> *Le début de l'énoncé n'apparaît pas sur la photo : seule la fin de l'exemple détaillé et la partie Implementation sont visibles. À compléter si tu retrouves la capture.*

**Fin de l'exemple détaillé (visible) :**

- The correct number of clusters is 3.
- The total size of these clusters is (512 \* 3 = 1536 bytes), which is the size on disk of this file.

### Implementation

**Function** — Implement the function `compute_size_on_disk`.

**Parameters**

| Name | Type | Description |
|---|---|---|
| `cluster_size` | int | The cluster size of a disk (in bytes). |
| `file_size` | int | The size of a file (in bytes). |

**Return value**

| Name | Type | Description |
|---|---|---|
| `file_size_on_disk` | int | The 'size on disk' of this file, on this disk (in bytes). |

**Constraints**

- 1 <= cluster_size <= 65,536
- 0 <= file_size <= 1,000,000
- Available RAM: 512MB
- Timeout: 6 seconds

**Example**

| Parameters | Return value |
|---|---|
| `512, 1500` | `1536` |
