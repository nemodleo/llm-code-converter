"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = __importStar(require("vscode"));
const axios_1 = __importDefault(require("axios"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const child_process_1 = require("child_process");
// 공통 설정
const DEFAULT_PROJECT_PATH = '/Users/nemo/Documents/창의적통합설계2/snucse_2501_aiconvertor/samples/cvt-spring-boot-map';
const DEFAULT_OUTPUT_PATH = '/Users/nemo/Documents/창의적통합설계2/snucse_2501_aiconvertor/samples/cvt-spring-boot-map/vo';
// 로그 관리자 클래스
class LogManager {
    constructor() {
        this.serverProcess = null;
        this.serverPath = '';
        this.isWatchingLogFile = false;
        this.logFilePath = '';
        this.lastLogPosition = 0;
        this.outputChannel = vscode.window.createOutputChannel('LLM Server Logs');
    }
    static getInstance() {
        if (!LogManager.instance) {
            LogManager.instance = new LogManager();
        }
        return LogManager.instance;
    }
    log(message, level = 'INFO') {
        const timestamp = new Date().toISOString();
        const logMessage = `[${timestamp}] [${level}] ${message}`;
        this.outputChannel.appendLine(logMessage);
        console.log(logMessage);
    }
    show() {
        this.outputChannel.show();
    }
    clear() {
        this.outputChannel.clear();
        this.lastLogPosition = 0;
    }
    async startLogFileMonitoring(logFilePath) {
        this.log('=== Starting log file monitoring process ===', 'INFO');
        if (logFilePath) {
            this.logFilePath = logFilePath;
            this.log(`Using provided log file path: ${logFilePath}`, 'INFO');
        }
        else {
            this.log('No log file path provided, using hardcoded macOS path...', 'INFO');
            const hardcodedLogPath = '/Users/nemo/Library/Logs/llm_converter/server.log';
            if (fs.existsSync(hardcodedLogPath)) {
                this.logFilePath = hardcodedLogPath;
                this.log(`✅ Using hardcoded macOS log path (file exists): ${hardcodedLogPath}`, 'INFO');
            }
            else {
                this.logFilePath = hardcodedLogPath;
                this.log(`⚠️ Using hardcoded macOS log path (file doesn't exist yet): ${hardcodedLogPath}`, 'WARN');
            }
        }
        if (!this.logFilePath) {
            this.log('❌ Could not determine log file path', 'ERROR');
            vscode.window.showErrorMessage('Could not determine log file path. Please set it manually.');
            return;
        }
        this.log(`📁 Final log file path: ${this.logFilePath}`, 'INFO');
        this.log(`📄 File exists: ${fs.existsSync(this.logFilePath)}`, 'INFO');
        if (fs.existsSync(this.logFilePath)) {
            const stats = fs.statSync(this.logFilePath);
            this.log(`📊 File size: ${stats.size} bytes`, 'INFO');
            this.log(`🕒 Last modified: ${stats.mtime}`, 'INFO');
        }
        this.readExistingLogFile();
        try {
            if (this.isWatchingLogFile) {
                this.log('Stopping existing file watcher...', 'INFO');
                fs.unwatchFile(this.logFilePath);
            }
            this.isWatchingLogFile = true;
            fs.watchFile(this.logFilePath, { interval: 1000 }, (curr, prev) => {
                if (curr.mtime !== prev.mtime) {
                    this.log('📝 Log file changed, reading new content...', 'DEBUG');
                    this.readNewLogContent();
                }
            });
            this.log('✅ Log file monitoring started successfully', 'INFO');
            this.log('=== Log file monitoring setup complete ===', 'INFO');
            vscode.window.showInformationMessage(`Log monitoring started: ${path.basename(this.logFilePath)}`);
        }
        catch (error) {
            this.log(`❌ Failed to start log file monitoring: ${error}`, 'ERROR');
            this.isWatchingLogFile = false;
        }
    }
    readExistingLogFile() {
        try {
            if (fs.existsSync(this.logFilePath)) {
                const content = fs.readFileSync(this.logFilePath, 'utf8');
                if (content.trim()) {
                    this.outputChannel.appendLine('=== Existing Log Content ===');
                    this.outputChannel.appendLine(content);
                    this.outputChannel.appendLine('=== Live Log Updates ===');
                    this.lastLogPosition = content.length;
                }
                else {
                    this.lastLogPosition = 0;
                }
            }
            else {
                this.log('Log file does not exist yet, waiting for creation...', 'INFO');
                this.lastLogPosition = 0;
            }
        }
        catch (error) {
            this.log(`Error reading existing log file: ${error}`, 'ERROR');
            this.lastLogPosition = 0;
        }
    }
    readNewLogContent() {
        try {
            if (fs.existsSync(this.logFilePath)) {
                const stats = fs.statSync(this.logFilePath);
                if (stats.size > this.lastLogPosition) {
                    const stream = fs.createReadStream(this.logFilePath, {
                        start: this.lastLogPosition,
                        encoding: 'utf8'
                    });
                    let newContent = '';
                    stream.on('data', (chunk) => {
                        newContent += chunk;
                    });
                    stream.on('end', () => {
                        if (newContent.trim()) {
                            const lines = newContent.trim().split('\n');
                            lines.forEach(line => {
                                if (line.trim()) {
                                    this.outputChannel.appendLine(`[SERVER] ${line}`);
                                }
                            });
                        }
                        this.lastLogPosition = stats.size;
                    });
                    stream.on('error', (error) => {
                        this.log(`Error reading new log content: ${error}`, 'ERROR');
                    });
                }
            }
        }
        catch (error) {
            this.log(`Error monitoring log file: ${error}`, 'ERROR');
        }
    }
    stopLogFileMonitoring() {
        if (this.isWatchingLogFile) {
            fs.unwatchFile(this.logFilePath);
            this.isWatchingLogFile = false;
            this.log('Log file monitoring stopped', 'INFO');
        }
    }
    async setLogFilePath() {
        const hardcodedPath = '/Users/nemo/Library/Logs/llm_converter/server.log';
        const result = await vscode.window.showInputBox({
            prompt: 'Enter path to server log file (server.log)',
            value: hardcodedPath,
            placeHolder: '/Users/nemo/Library/Logs/llm_converter/server.log'
        });
        if (result) {
            this.logFilePath = result;
            this.log(`🔨 HARDCODED: Log file path set to: ${result}`, 'INFO');
            this.stopLogFileMonitoring();
            this.startLogFileMonitoring(result);
        }
    }
    async startServer(serverPath) {
        if (this.serverProcess) {
            this.log('Server is already running', 'WARN');
            return true;
        }
        const pythonPath = serverPath || this.findServerPath();
        if (!pythonPath) {
            this.log('Python server file not found. Please set server path manually.', 'ERROR');
            return false;
        }
        this.serverPath = pythonPath;
        this.log(`Starting Python server: ${pythonPath}`, 'INFO');
        try {
            this.serverProcess = (0, child_process_1.spawn)('python', [pythonPath], {
                cwd: path.dirname(pythonPath),
                stdio: ['pipe', 'pipe', 'pipe']
            });
            this.serverProcess.stdout?.on('data', (data) => {
                const output = data.toString().trim();
                if (output) {
                    this.log(`[SERVER STDOUT] ${output}`, 'INFO');
                }
            });
            this.serverProcess.stderr?.on('data', (data) => {
                const output = data.toString().trim();
                if (output) {
                    this.log(`[SERVER STDERR] ${output}`, 'ERROR');
                }
            });
            this.serverProcess.on('close', (code) => {
                this.log(`Server process exited with code ${code}`, code === 0 ? 'INFO' : 'ERROR');
                this.serverProcess = null;
            });
            this.serverProcess.on('error', (error) => {
                this.log(`Failed to start server: ${error.message}`, 'ERROR');
                this.serverProcess = null;
            });
            await new Promise(resolve => setTimeout(resolve, 2000));
            const hardcodedLogPath = '/Users/nemo/Library/Logs/llm_converter/server.log';
            this.log(`🔨 HARDCODED: Starting log monitoring after server start: ${hardcodedLogPath}`, 'INFO');
            this.startLogFileMonitoring(hardcodedLogPath);
            this.log('Server started successfully', 'INFO');
            return true;
        }
        catch (error) {
            this.log(`Error starting server: ${error}`, 'ERROR');
            return false;
        }
    }
    stopServer() {
        this.stopLogFileMonitoring();
        if (this.serverProcess) {
            this.log('Stopping Python server...', 'INFO');
            this.serverProcess.kill();
            this.serverProcess = null;
            this.log('Server stopped', 'INFO');
        }
        else {
            this.log('No server process to stop', 'WARN');
        }
    }
    isServerRunning() {
        return this.serverProcess !== null;
    }
    findServerPath() {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            return null;
        }
        const commonPaths = [
            'server.py',
            'src/server.py',
            'backend/server.py',
            'api/server.py',
            'llm_pipeline.py',
            'src/llm_pipeline.py'
        ];
        for (const folder of workspaceFolders) {
            for (const relativePath of commonPaths) {
                const fullPath = path.join(folder.uri.fsPath, relativePath);
                if (fs.existsSync(fullPath)) {
                    this.serverPath = fullPath;
                    return fullPath;
                }
            }
        }
        return null;
    }
    async setServerPath() {
        const result = await vscode.window.showInputBox({
            prompt: 'Enter path to Python server file (server.py or llm_pipeline.py)',
            value: this.serverPath || this.findServerPath() || '',
            placeHolder: '/path/to/server.py'
        });
        if (result && fs.existsSync(result)) {
            this.serverPath = result;
            this.log(`Server path set to: ${result}`, 'INFO');
            this.logFilePath = '/Users/nemo/Library/Logs/llm_converter/server.log';
            this.log(`🔨 HARDCODED: Log file path updated to: ${this.logFilePath}`, 'INFO');
        }
        else if (result) {
            this.log(`Invalid server path: ${result}`, 'ERROR');
        }
    }
    getServerPath() {
        return this.serverPath;
    }
    getLogFilePath() {
        return this.logFilePath || '/Users/nemo/Library/Logs/llm_converter/server.log';
    }
    isMonitoringLogFile() {
        return this.isWatchingLogFile;
    }
}
// LLM API 클라이언트
class LLMCodeConverter {
    constructor() {
        const config = vscode.workspace.getConfiguration('llmCodeConverter');
        this.apiEndpoint = config.get('apiEndpoint', 'http://localhost:8000');
        this.timeout = config.get('timeout', 30000000);
        this.logManager = LogManager.getInstance();
    }
    async convertCode(fullFileContent, targetLanguage, sourceLanguage, filePath, startLine, endLine) {
        this.logManager.log(`Starting code conversion: lines ${startLine}-${endLine} to ${targetLanguage}`);
        try {
            const request = {
                source_code: fullFileContent,
                target_language: targetLanguage,
                source_language: sourceLanguage,
                file_path: filePath,
                start_line: startLine,
                end_line: endLine
            };
            this.logManager.log(`Sending request to ${this.apiEndpoint}/convert-code`);
            const response = await axios_1.default.post(`${this.apiEndpoint}/convert-code`, request, {
                timeout: this.timeout,
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            this.logManager.log(`Code conversion completed successfully in ${response.data.processing_time?.toFixed(2)}s`);
            return response.data;
        }
        catch (error) {
            this.logManager.log(`Code conversion failed: ${error}`, 'ERROR');
            throw new Error(`API request failed: ${error}`);
        }
    }
    async convertCodeWithVO(fullFileContent, targetLanguage, sourceLanguage, filePath, startLine, endLine, voPath) {
        this.logManager.log(`Starting code conversion to VO: lines ${startLine}-${endLine}, VO path: ${voPath}`);
        try {
            const request = {
                source_code: fullFileContent,
                target_language: targetLanguage,
                source_language: sourceLanguage,
                file_path: filePath,
                start_line: startLine,
                end_line: endLine,
                vo_path: voPath
            };
            this.logManager.log(`Sending request to ${this.apiEndpoint}/convert-code with VO path`);
            const response = await axios_1.default.post(`${this.apiEndpoint}/convert-code`, request, {
                timeout: this.timeout,
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            this.logManager.log(`VO conversion completed successfully in ${response.data.processing_time?.toFixed(2)}s`);
            return response.data;
        }
        catch (error) {
            this.logManager.log(`VO conversion failed: ${error}`, 'ERROR');
            throw new Error(`API request failed: ${error}`);
        }
    }
    async makeVO(projectPath, voPath) {
        this.logManager.log(`Starting VO generation for project: ${projectPath}, output: ${voPath}`);
        try {
            const request = {
                project_path: projectPath,
                vo_path: voPath
            };
            this.logManager.log(`Sending request to ${this.apiEndpoint}/make-vo`);
            const response = await axios_1.default.post(`${this.apiEndpoint}/make-vo`, request, {
                timeout: this.timeout,
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            this.logManager.log(`VO generation completed successfully: ${response.data.file_count} files processed in ${response.data.processing_time?.toFixed(2)}s`);
            return response.data;
        }
        catch (error) {
            this.logManager.log(`VO generation failed: ${error}`, 'ERROR');
            throw new Error(`Make VO API request failed: ${error}`);
        }
    }
    async checkHealth() {
        try {
            this.logManager.log('Checking API health...');
            const response = await axios_1.default.get(`${this.apiEndpoint}/health`, {
                timeout: 5000
            });
            const isHealthy = response.status === 200;
            this.logManager.log(`API health check: ${isHealthy ? 'ONLINE' : 'OFFLINE'}`, isHealthy ? 'INFO' : 'WARN');
            return isHealthy;
        }
        catch (error) {
            this.logManager.log(`API health check failed: ${error}`, 'ERROR');
            return false;
        }
    }
}
// 공통 아이템 클래스
class BaseItem extends vscode.TreeItem {
    constructor(label, collapsibleState, iconPath, description, itemType, commandId) {
        super(label, collapsibleState);
        this.label = label;
        this.collapsibleState = collapsibleState;
        this.iconPath = iconPath;
        this.description = description;
        this.itemType = itemType;
        this.commandId = commandId;
        this.tooltip = `${this.label}: ${this.description}`;
        this.description = description;
        if (commandId) {
            this.command = {
                command: commandId,
                title: this.label
            };
        }
    }
}
// VO Generator Provider (첫 번째 탭)
class VOGeneratorProvider {
    constructor() {
        this._onDidChangeTreeData = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
        this.projectPath = DEFAULT_PROJECT_PATH;
        this.outputPath = DEFAULT_OUTPUT_PATH;
        this.analysisResult = 'No analysis performed yet';
        this.fileCount = 0;
        this.lastRunStatus = 'idle';
    }
    refresh() {
        this._onDidChangeTreeData.fire();
    }
    getTreeItem(element) {
        return element;
    }
    getChildren(element) {
        if (!element) {
            return Promise.resolve([
                new BaseItem('📁 Project Path', vscode.TreeItemCollapsibleState.None, 'folder', this.projectPath || 'Click to set project path', 'project-path', 'llm-code-converter.setProjectPath'),
                new BaseItem('📂 Output Path', vscode.TreeItemCollapsibleState.None, 'folder-opened', this.outputPath || 'Click to set output path', 'output-path', 'llm-code-converter.setOutputPath'),
                new BaseItem('📊 File Count', vscode.TreeItemCollapsibleState.None, 'file', `${this.fileCount} files`),
                new BaseItem('🔄 Status', vscode.TreeItemCollapsibleState.None, this.getStatusIcon(), this.getStatusText()),
                new BaseItem('📋 Last Result', vscode.TreeItemCollapsibleState.Collapsed, 'output', this.analysisResult)
            ]);
        }
        else if (element.label === '📋 Last Result') {
            return Promise.resolve([
                new BaseItem(this.analysisResult, vscode.TreeItemCollapsibleState.None, 'info', '')
            ]);
        }
        return Promise.resolve([]);
    }
    getStatusIcon() {
        switch (this.lastRunStatus) {
            case 'running': return 'loading~spin';
            case 'success': return 'check';
            case 'error': return 'error';
            default: return 'circle-outline';
        }
    }
    getStatusText() {
        switch (this.lastRunStatus) {
            case 'running': return 'Running VO generation...';
            case 'success': return 'VO generation completed';
            case 'error': return 'VO generation failed';
            default: return 'Ready to generate VO';
        }
    }
    async setProjectPath() {
        const result = await vscode.window.showInputBox({
            prompt: 'Enter project path for VO generation',
            value: this.projectPath || DEFAULT_PROJECT_PATH,
            placeHolder: DEFAULT_PROJECT_PATH
        });
        if (result) {
            this.projectPath = result;
            this.countFiles();
            this.refresh();
            if (codeConverterProvider) {
                codeConverterProvider.updateProjectPath(result);
            }
        }
    }
    async setOutputPath() {
        const result = await vscode.window.showInputBox({
            prompt: 'Enter output path for generated VO files',
            value: this.outputPath || DEFAULT_OUTPUT_PATH,
            placeHolder: DEFAULT_OUTPUT_PATH
        });
        if (result) {
            this.outputPath = result;
            this.refresh();
            if (codeConverterProvider) {
                codeConverterProvider.updateVOPath(result);
            }
        }
    }
    countFiles() {
        if (!this.projectPath || !fs.existsSync(this.projectPath)) {
            this.fileCount = 0;
            return;
        }
        try {
            const files = this.getAllFiles(this.projectPath);
            this.fileCount = files.length;
        }
        catch (error) {
            this.fileCount = 0;
        }
    }
    getAllFiles(dirPath) {
        const files = [];
        try {
            const items = fs.readdirSync(dirPath);
            for (const item of items) {
                const fullPath = path.join(dirPath, item);
                const stat = fs.statSync(fullPath);
                if (stat.isDirectory()) {
                    if (!['node_modules', '.git', '.vscode', '__pycache__', 'out', 'dist'].includes(item)) {
                        files.push(...this.getAllFiles(fullPath));
                    }
                }
                else {
                    const ext = path.extname(item).toLowerCase();
                    if (['.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go', '.rs', '.php'].includes(ext)) {
                        files.push(fullPath);
                    }
                }
            }
        }
        catch (error) {
            console.error('Error reading directory:', error);
        }
        return files;
    }
    async runAnalysis() {
        this.log('🔍 VO Generation: Starting analysis...');
        if (!this.projectPath) {
            this.log('❌ VO Generation: No project path set');
            vscode.window.showErrorMessage('Please set project path first');
            return;
        }
        this.log(`📁 VO Generation: Project path = ${this.projectPath}`);
        if (!fs.existsSync(this.projectPath)) {
            this.log(`❌ VO Generation: Project path does not exist: ${this.projectPath}`);
            vscode.window.showErrorMessage('Project path does not exist');
            return;
        }
        if (!this.outputPath) {
            this.log('❌ VO Generation: No output path set');
            vscode.window.showErrorMessage('Please set output path first');
            return;
        }
        this.log(`📂 VO Generation: Output path = ${this.outputPath}`);
        this.lastRunStatus = 'running';
        this.refresh();
        try {
            this.log('🌐 VO Generation: Creating API client...');
            const converter = new LLMCodeConverter();
            this.log('🔍 VO Generation: Checking API health...');
            const isHealthy = await converter.checkHealth();
            if (!isHealthy) {
                throw new Error('LLM API is not available. Please check if the server is running.');
            }
            this.log('✅ VO Generation: API is healthy, calling make-vo...');
            const result = await converter.makeVO(this.projectPath, this.outputPath);
            this.log(`📊 VO Generation: API response - success: ${result.success}`);
            this.log(`📊 VO Generation: API response - file_count: ${result.file_count}`);
            this.log(`📊 VO Generation: API response - processing_time: ${result.processing_time}`);
            if (result.success) {
                this.fileCount = result.file_count;
                this.analysisResult = `VO generated successfully!\nProject: ${this.projectPath}\nOutput: ${this.outputPath}\nFiles: ${result.file_count}\nTime: ${result.processing_time.toFixed(2)}s`;
                this.lastRunStatus = 'success';
                this.log('💾 VO Generation: Saving VO file...');
                await this.saveVOFile(result.vo_code);
                this.log('📄 VO Generation: Creating new document...');
                const doc = await vscode.workspace.openTextDocument({
                    content: result.vo_code,
                    language: 'java'
                });
                await vscode.window.showTextDocument(doc);
                this.log('✅ VO Generation: Completed successfully!');
                vscode.window.showInformationMessage(`VO generated successfully! Found ${result.file_count} files in ${result.processing_time.toFixed(2)}s`);
            }
            else {
                this.log(`❌ VO Generation: API returned error - ${result.message}`);
                throw new Error(result.message);
            }
        }
        catch (error) {
            this.log(`❌ VO Generation: Error occurred - ${error}`);
            this.analysisResult = `Error: ${error}`;
            this.lastRunStatus = 'error';
            vscode.window.showErrorMessage(`VO generation failed: ${error}`);
        }
        this.refresh();
    }
    async saveVOFile(voCode) {
        try {
            if (!fs.existsSync(this.outputPath)) {
                fs.mkdirSync(this.outputPath, { recursive: true });
            }
            const projectName = path.basename(this.projectPath).replace(/[^a-zA-Z0-9]/g, '_');
            const fileName = `${projectName}VO.java`;
            const filePath = path.join(this.outputPath, fileName);
            fs.writeFileSync(filePath, voCode, 'utf-8');
            vscode.window.showInformationMessage(`VO file saved to: ${filePath}`);
        }
        catch (error) {
            vscode.window.showErrorMessage(`Failed to save VO file: ${error}`);
        }
    }
    log(message) {
        const logManager = LogManager.getInstance();
        logManager.log(`[VO-PROVIDER] ${message}`, 'INFO');
    }
    getProjectPath() {
        return this.projectPath;
    }
    updateOutputPath(newPath) {
        this.outputPath = newPath;
        this.refresh();
    }
}
// Code Converter Provider (두 번째 탭)
class CodeConverterProvider {
    constructor() {
        this._onDidChangeTreeData = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
        this.lastConversion = 'No conversion performed yet';
        this.conversionHistory = [];
        this.apiStatus = 'unknown';
        this.projectPath = DEFAULT_PROJECT_PATH;
        this.voPath = DEFAULT_OUTPUT_PATH;
        this.logManager = LogManager.getInstance();
    }
    refresh() {
        this.checkAPIStatus();
        this._onDidChangeTreeData.fire();
    }
    getTreeItem(element) {
        return element;
    }
    getChildren(element) {
        if (!element) {
            return Promise.resolve([
                new BaseItem('🌐 API Status', vscode.TreeItemCollapsibleState.None, this.getAPIStatusIcon(), this.getAPIStatusText()),
                new BaseItem('🔄 Map to VO', vscode.TreeItemCollapsibleState.None, 'arrow-right', 'Select code and map to VO', 'convert', 'llm-code-converter.convertCode'),
                new BaseItem('📁 Project Path', vscode.TreeItemCollapsibleState.None, 'folder', this.projectPath, 'project-path', 'llm-code-converter.setProjectPath'),
                new BaseItem('📄 VO Path', vscode.TreeItemCollapsibleState.None, 'file-code', this.voPath, 'vo-path', 'llm-code-converter.setVOPath'),
                new BaseItem('📝 Last Conversion', vscode.TreeItemCollapsibleState.None, 'file-text', this.lastConversion),
                new BaseItem('📚 History', vscode.TreeItemCollapsibleState.Collapsed, 'history', `${this.conversionHistory.length} conversions`),
                new BaseItem('🖥️ Server Control', vscode.TreeItemCollapsibleState.Expanded, 'server', this.logManager.isServerRunning() ? 'Server Running' : 'Server Stopped'),
                new BaseItem('📋 View Logs', vscode.TreeItemCollapsibleState.None, 'output', 'Show server logs', 'logs', 'llm-code-converter.showLogs'),
                new BaseItem('⚙️ Settings', vscode.TreeItemCollapsibleState.Collapsed, 'gear', 'API configuration')
            ]);
        }
        else if (element.label === '📚 History') {
            return Promise.resolve(this.conversionHistory.slice(-5).reverse().map((item, index) => new BaseItem(`${index + 1}. ${item}`, vscode.TreeItemCollapsibleState.None, 'file', '')));
        }
        else if (element.label === '🖥️ Server Control') {
            const isRunning = this.logManager.isServerRunning();
            const isMonitoring = this.logManager.isMonitoringLogFile();
            return Promise.resolve([
                new BaseItem('📁 Set Server Path', vscode.TreeItemCollapsibleState.None, 'folder', this.logManager.getServerPath() || 'Click to set', 'server-path', 'llm-code-converter.setServerPath'),
                new BaseItem('📋 Set Log File Path', vscode.TreeItemCollapsibleState.None, 'file', this.logManager.getLogFilePath() || 'Auto-detect', 'log-path', 'llm-code-converter.setLogFilePath'),
                new BaseItem(isRunning ? '⏹️ Stop Server' : '▶️ Start Server', vscode.TreeItemCollapsibleState.None, isRunning ? 'stop' : 'play', '', 'server-control', isRunning ? 'llm-code-converter.stopServer' : 'llm-code-converter.startServer'),
                new BaseItem('🔄 Restart Server', vscode.TreeItemCollapsibleState.None, 'refresh', 'Restart Python server', 'restart', 'llm-code-converter.restartServer'),
                new BaseItem(isMonitoring ? '👁️ Stop Log Monitoring' : '👁️ Start Log Monitoring', vscode.TreeItemCollapsibleState.None, isMonitoring ? 'eye-closed' : 'eye', isMonitoring ? 'Stop monitoring log file' : 'Start monitoring log file', 'log-monitor', isMonitoring ? 'llm-code-converter.stopLogMonitoring' : 'llm-code-converter.startLogMonitoring')
            ]);
        }
        else if (element.label === '⚙️ Settings') {
            const config = vscode.workspace.getConfiguration('llmCodeConverter');
            return Promise.resolve([
                new BaseItem('API Endpoint', vscode.TreeItemCollapsibleState.None, 'link', config.get('apiEndpoint', 'http://localhost:8000')),
                new BaseItem('Timeout', vscode.TreeItemCollapsibleState.None, 'clock', `${config.get('timeout', 300000000)}ms`)
            ]);
        }
        return Promise.resolve([]);
    }
    async checkAPIStatus() {
        try {
            const converter = new LLMCodeConverter();
            const isHealthy = await converter.checkHealth();
            this.apiStatus = isHealthy ? 'online' : 'offline';
        }
        catch (error) {
            this.apiStatus = 'offline';
        }
    }
    getAPIStatusIcon() {
        switch (this.apiStatus) {
            case 'online': return 'check';
            case 'offline': return 'error';
            default: return 'question';
        }
    }
    getAPIStatusText() {
        switch (this.apiStatus) {
            case 'online': return 'API Server Online';
            case 'offline': return 'API Server Offline';
            default: return 'Checking API...';
        }
    }
    addConversionHistory(description) {
        const timestamp = new Date().toLocaleTimeString();
        this.conversionHistory.push(`${timestamp}: ${description}`);
        this.lastConversion = description;
        this.refresh();
    }
    updateProjectPath(newPath) {
        this.projectPath = newPath;
        this.refresh();
    }
    updateVOPath(newPath) {
        this.voPath = newPath;
        this.refresh();
    }
    async setVOPath() {
        const result = await vscode.window.showInputBox({
            prompt: 'Enter VO output file path',
            value: this.voPath || DEFAULT_OUTPUT_PATH,
            placeHolder: DEFAULT_OUTPUT_PATH
        });
        if (result) {
            this.voPath = result;
            this.refresh();
            if (voGeneratorProvider) {
                voGeneratorProvider.updateOutputPath(result);
            }
        }
    }
    getProjectPath() {
        return this.projectPath;
    }
    getVOPath() {
        return this.voPath;
    }
    log(message) {
        const logManager = LogManager.getInstance();
        logManager.log(`[CODE-CONVERTER] ${message}`, 'INFO');
    }
}
// 코드 변환 명령 (드래그한 부분을 VO로 변환)
async function convertCodeCommand() {
    const converter = new LLMCodeConverter();
    const isHealthy = await converter.checkHealth();
    if (!isHealthy) {
        vscode.window.showErrorMessage('LLM API is not available. Please check if the server is running.');
        return;
    }
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor found');
        return;
    }
    const selection = editor.selection;
    if (selection.isEmpty) {
        vscode.window.showErrorMessage('Please select the code you want to map to VO');
        return;
    }
    const fullFileContent = editor.document.getText();
    const startLine = selection.start.line + 1;
    const endLine = selection.end.line + 1;
    const filePath = editor.document.fileName;
    if (!fullFileContent.trim()) {
        vscode.window.showErrorMessage('No file content');
        return;
    }
    const voPath = codeConverterProvider ? codeConverterProvider.getVOPath() : DEFAULT_OUTPUT_PATH;
    const targetLanguage = 'java';
    try {
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Mapping code to VO...',
            cancellable: false
        }, async (progress) => {
            progress.report({ increment: 50, message: 'Processing...' });
            const result = await converter.convertCodeWithVO(fullFileContent, targetLanguage, undefined, filePath, startLine, endLine, voPath);
            progress.report({ increment: 50, message: 'Creating new document...' });
            if (result.success) {
                const doc = await vscode.workspace.openTextDocument({
                    content: result.converted_code,
                    language: 'java'
                });
                await vscode.window.showTextDocument(doc);
                if (codeConverterProvider) {
                    codeConverterProvider.addConversionHistory(`Lines ${startLine}-${endLine} → Java VO`);
                }
                vscode.window.showInformationMessage(`Lines ${startLine}-${endLine} mapped to VO successfully!`);
            }
            else {
                vscode.window.showErrorMessage(`Conversion failed: ${result.message}`);
            }
        });
    }
    catch (error) {
        vscode.window.showErrorMessage(`Conversion failed: ${error}`);
    }
}
// 전역 변수로 provider 참조 저장
let voGeneratorProvider;
let codeConverterProvider;
function activate(context) {
    console.log('🚀 LLM Code Converter extension is now active!');
    const logManager = LogManager.getInstance();
    logManager.log('Extension activated', 'INFO');
    voGeneratorProvider = new VOGeneratorProvider();
    codeConverterProvider = new CodeConverterProvider();
    const convertCodeDisposable = vscode.commands.registerCommand('llm-code-converter.convertCode', convertCodeCommand);
    const generateVODisposable = vscode.commands.registerCommand('llm-code-converter.generateVO', () => {
        logManager.log('🚀 VO Generation: Command triggered from UI', 'INFO');
        voGeneratorProvider.runAnalysis();
    });
    const refreshViewDisposable = vscode.commands.registerCommand('llm-code-converter.refreshView', () => {
        voGeneratorProvider.refresh();
    });
    const refreshConverterDisposable = vscode.commands.registerCommand('llm-code-converter.refreshConverter', () => {
        codeConverterProvider.refresh();
    });
    const setProjectPathDisposable = vscode.commands.registerCommand('llm-code-converter.setProjectPath', () => {
        voGeneratorProvider.setProjectPath();
    });
    const setOutputPathDisposable = vscode.commands.registerCommand('llm-code-converter.setOutputPath', () => {
        voGeneratorProvider.setOutputPath();
    });
    const setVOPathDisposable = vscode.commands.registerCommand('llm-code-converter.setVOPath', () => {
        codeConverterProvider.setVOPath();
    });
    const setServerPathDisposable = vscode.commands.registerCommand('llm-code-converter.setServerPath', () => {
        logManager.setServerPath();
    });
    const setLogFilePathDisposable = vscode.commands.registerCommand('llm-code-converter.setLogFilePath', () => {
        logManager.setLogFilePath();
    });
    const startLogMonitoringDisposable = vscode.commands.registerCommand('llm-code-converter.startLogMonitoring', async () => {
        const hardcodedLogPath = '/Users/nemo/Library/Logs/llm_converter/server.log';
        logManager.log(`🔨 HARDCODED: Starting log monitoring with: ${hardcodedLogPath}`, 'INFO');
        await logManager.startLogFileMonitoring(hardcodedLogPath);
        codeConverterProvider.refresh();
    });
    const startLogMonitoringDirectDisposable = vscode.commands.registerCommand('llm-code-converter.startLogMonitoringDirect', async () => {
        const macOSLogPath = '/Users/nemo/Library/Logs/llm_converter/server.log';
        logManager.log(`Attempting to monitor log file directly: ${macOSLogPath}`, 'INFO');
        await logManager.startLogFileMonitoring(macOSLogPath);
        codeConverterProvider.refresh();
        vscode.window.showInformationMessage('Direct log monitoring started');
    });
    const stopLogMonitoringDisposable = vscode.commands.registerCommand('llm-code-converter.stopLogMonitoring', () => {
        logManager.stopLogFileMonitoring();
        codeConverterProvider.refresh();
        vscode.window.showInformationMessage('Log file monitoring stopped');
    });
    const startServerDisposable = vscode.commands.registerCommand('llm-code-converter.startServer', async () => {
        logManager.log('Starting server command triggered', 'INFO');
        const success = await logManager.startServer();
        if (success) {
            vscode.window.showInformationMessage('Python server started successfully');
            codeConverterProvider.refresh();
        }
        else {
            vscode.window.showErrorMessage('Failed to start Python server. Check logs for details.');
        }
    });
    const stopServerDisposable = vscode.commands.registerCommand('llm-code-converter.stopServer', () => {
        logManager.log('Stopping server command triggered', 'INFO');
        logManager.stopServer();
        vscode.window.showInformationMessage('Python server stopped');
        codeConverterProvider.refresh();
    });
    const restartServerDisposable = vscode.commands.registerCommand('llm-code-converter.restartServer', async () => {
        logManager.log('Restarting server command triggered', 'INFO');
        logManager.stopServer();
        await new Promise(resolve => setTimeout(resolve, 1000));
        const success = await logManager.startServer();
        if (success) {
            vscode.window.showInformationMessage('Python server restarted successfully');
        }
        else {
            vscode.window.showErrorMessage('Failed to restart Python server. Check logs for details.');
        }
        codeConverterProvider.refresh();
    });
    const showLogsDisposable = vscode.commands.registerCommand('llm-code-converter.showLogs', () => {
        logManager.show();
    });
    const clearLogsDisposable = vscode.commands.registerCommand('llm-code-converter.clearLogs', () => {
        logManager.clear();
        logManager.log('Logs cleared', 'INFO');
    });
    const voTreeView = vscode.window.createTreeView('voGeneratorView', {
        treeDataProvider: voGeneratorProvider,
        showCollapseAll: true
    });
    const converterTreeView = vscode.window.createTreeView('codeConverterView', {
        treeDataProvider: codeConverterProvider,
        showCollapseAll: true
    });
    context.subscriptions.push(convertCodeDisposable, generateVODisposable, refreshViewDisposable, refreshConverterDisposable, setProjectPathDisposable, setOutputPathDisposable, setVOPathDisposable, setServerPathDisposable, setLogFilePathDisposable, startLogMonitoringDisposable, startLogMonitoringDirectDisposable, stopLogMonitoringDisposable, startServerDisposable, stopServerDisposable, restartServerDisposable, showLogsDisposable, clearLogsDisposable, voTreeView, converterTreeView);
    logManager.log('All commands and views registered successfully', 'INFO');
    const autoStartLogPath = '/Users/nemo/Library/Logs/llm_converter/server.log';
    logManager.log(`🔨 AUTO-START: Starting log monitoring automatically: ${autoStartLogPath}`, 'INFO');
    setTimeout(async () => {
        await logManager.startLogFileMonitoring(autoStartLogPath);
        codeConverterProvider.refresh();
    }, 1000);
    console.log('✅ LLM Code Converter extension successfully activated!');
    vscode.window.showInformationMessage('LLM Code Converter is ready!');
}
exports.activate = activate;
function deactivate() {
    console.log('👋 LLM Code Converter extension deactivated!');
    const logManager = LogManager.getInstance();
    logManager.stopLogFileMonitoring();
    logManager.stopServer();
    logManager.log('Extension deactivated', 'INFO');
}
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map