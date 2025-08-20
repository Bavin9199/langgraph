# Lang Graph

## 1 Type Annotations

### 1.1 Typed dictionary

### 1.2 Union & Optional

### 1.3 Any

### 1.4 lambda function (map function)

## 2 Elements

### 2.1 state

### 2.2 nodes

receive and execute states

### 2.3 graph

show nodes how to connect![image-20250819102817142](C:\Users\haoxie\AppData\Roaming\Typora\typora-user-images\image-20250819102817142.png)

### 2.4 edges

tell which node should be executed next

### 2.5 conditional edges

connections based on specific condition or logic

### 2.6 start

start node (virtual entry point)

### 2.7 end

the conclusion of the workflow

all completed until this

### 2.8 tools

specialized functions and utilizes

### 2.9 toolnode

special kind of node to run a tool

return the tool's output back to state for other nodes to use

### 2.10 stategraph

build and compile the graph structure

manages nodes, edges, states and workflow operate in a unified way

### 2.11 runnable

component performs a specific tasks with AI workflow

runnable: represent various action

nodes: receive, perform and execute the states

### 2.12 messages

#### 2.12.1 message types

human message: input

ai message: response

system message: provide instructions or context to the model

tool message: specific to tool usage

function message: function call

## 3 Code

### 3.1 

![image-20250819105919874](C:\Users\haoxie\AppData\Roaming\Typora\typora-user-images\image-20250819105919874.png)