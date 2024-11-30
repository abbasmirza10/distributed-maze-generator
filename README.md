### `README.md` for **distributed-maze-generator**

```markdown
# Distributed Maze Generator

A distributed infinite maze generator that collaborates with other services to create and visualize maze tiles in real-time. This project implements both static and dynamic maze generation using Python and aiohttp, with a focus on solvable paths and compliance with distributed middleware.

## Features
- **Static Maze Generation**: Generates a predefined 7×7 maze tile with consistent exits.
- **Dynamic Maze Generation**: Creates random 7×7 maze tiles with solvable paths based on specified exits.
- **Integration with Middleware**: Registers and interacts with a provided middleware to simulate a collaborative distributed maze.

## API Endpoints
### `GET /static`
- Returns the same 7×7 maze tile every time.
- The maze is represented as a JSON array of seven strings, where each string encodes walls in hexadecimal format.

Example:
```json
[
  "988088c",
  "1000004",
  "1000004",
  "0000000",
  "1000004",
  "1000004",
  "3220226"
]
```

### `GET /dynamic/<exit_code>`
- Returns a random 7×7 maze tile with a specific set of exits defined by `<exit_code>` (a hexadecimal value from `0` to `F`).
- Ensures solvability between all open exits.

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/abbasmirza10/distributed-maze-generator.git
   cd distributed-maze-generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the maze generator:
   ```bash
   make run
   ```

4. (Optional) Start both the maze generator and middleware for visualization:
   ```bash
   make view
   ```

## Testing
Run automated tests using:
```bash
make test
```

## File Structure
- `mazegen.py`: Implements the web service for static and dynamic maze generation.
- `mazelib.py`: Contains helper functions for maze generation.
- `mazeview.py`: Middleware for visualizing mazes (provided).

## Maze Encoding
Each cell in the maze is represented by a hexadecimal digit:
- **Bit 1 (1)**: Wall to the left.
- **Bit 2 (2)**: Wall at the bottom.
- **Bit 4 (4)**: Wall to the right.
- **Bit 8 (8)**: Wall at the top.

Example visualizations and codes:
| Hex Code | Cell Representation |
|----------|----------------------|
| `0`      | No walls            |
| `F`      | Fully walled         |

## Contributing
Contributions are welcome! Feel free to fork this repository, create a feature branch, and submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).

---
```
