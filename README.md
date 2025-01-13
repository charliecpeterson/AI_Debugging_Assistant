# AI Debugging Assistant

Just a small Langchain AI python code to debug errors in long text files

For this, I have a local Ollama server running.

Installing

```{bash}
pip install langchain ollama rich
```

Running

```{bash}
python diagnose_error.py path/to/error_log.txt
```

Save results

```{bash}
python diagnose_error.py path/to/error_log.txt --save results.txt
```

Interactive Mode

```{bash}
python diagnose_error.py
```

