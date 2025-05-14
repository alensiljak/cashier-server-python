#!/usr/bin/env python3
"""
Cashier Server - Ledger-cli REST server for Cashier PWA
FastAPI implementation
"""

import base64
import os
import subprocess
from typing import Optional
import uvicorn
from loguru import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create a FastAPI instance
app = FastAPI(
    title="Cashier Server",
    description="Ledger-cli REST server for Cashier PWA",
    version="0.4.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def index(query: str | None = None):
    '''Index. Based on the settings, it uses Ledger or Beancount for data.'''
    if not query:
        return {"error": "No query provided"}

    from dotenv import load_dotenv

    load_dotenv()
    bean_file = os.getenv('BEAN_FILE')
    if bean_file:
        return await beancount(query)
    else:
        return await ledger(query)


# @app.get("/")
async def ledger(query: Optional[str] = None):
    """
    Execute a ledger command and return the result.
    
    Args:
        query: The ledger command to execute
        
    Returns:
        The result of the ledger command
    """
    logger.info(f"Executing ledger query: {query}")

    try:
        # Execute the ledger command
        process = subprocess.run(
            ["ledger"] + query.split(),
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",
        )

        if process.returncode == 0:
            output = process.stdout
        else:
            output = process.stderr

        result = output.splitlines()
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing ledger command: {e}")
        return {"error": str(e), "stderr": e.stderr}

async def beancount(query: Optional[str] = None):
    """
    Execute a beancount query and return the result.
    Requires Beancount to be installed.

    Args:
        query: The beancount command to execute

    Returns:
        The result of the beancount command
    """
    bean_file = os.getenv('BEAN_FILE')
    if not bean_file:
        raise ValueError("BEAN_FILE environment variable not set")

    from beancount import loader
    # from beancount.query import query
    # import pandas as pd

    # todo: get the book file path.
    # Load your Beancount file
    entries, errors, options_map = loader.load_file(bean_file)

    # Run the query
    # row, rows = query.run(entries, options_map, query)
    # logger.debug(f"Query result: {rows}")
    # df = pd.DataFrame(rows)
    # print(df)

    # from beanquery.query import run_query
    # result = run_query('.tables')
    return entries

@app.get("/hello")
async def hello_img():
    """
    Return a base64-encoded image.
    """
    # This is a placeholder - you would need to replace with your actual image
    with open("hello.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

    return encoded_string

@app.get("/ping")
async def ping():
    """
    Simple ping endpoint to check if the server is running.
    """
    return "pong"

@app.get("/shutdown")
async def shutdown():
    """
    Shutdown the server.
    """
    logger.info("Shutdown requested")

    if hasattr(app.state, "server"):
        app.state.server.should_exit = True
        return {"message": "Server shut down"}
    else:
        return {"message": "Server not running"}


def main():
    '''
    Entry point for the executable script.
    '''
    logger.info("Starting Cashier Server on 0.0.0.0:3000")
    # Create a server instance that can be referenced
    # uvicorn.run(app, host="0.0.0.0", port=3000)
    config = uvicorn.Config(app, host="0.0.0.0", port=3000)
    server = uvicorn.Server(config)

    # Store the server instance in the app state
    app.state.server = server

    server.run()


if __name__ == "__main__":
    main()
