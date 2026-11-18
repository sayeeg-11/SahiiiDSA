import Editor from "@monaco-editor/react";

function CodeEditor({
  language = "python",
  value,
  onChange,
}) {
  return (
    <Editor
      height="450px"
      language={language}
      value={value}
      onChange={onChange}
      theme="vs-dark"
      options={{
        minimap: { enabled: false },
        fontSize: 14,
        automaticLayout: true,
        scrollBeyondLastLine: false,
        wordWrap: "on",
        tabSize: 4,
        padding: { top: 16 },
      }}
    />
  );
}

export default CodeEditor;