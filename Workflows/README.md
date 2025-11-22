# Workflows - n8n Automation Templates

This directory contains production-ready **n8n workflow templates** that demonstrate advanced AI-powered automation patterns. Unlike the code snippets in other folders, these are complete, runnable workflow automation templates in JSON format.

## Overview

**Purpose**: Provide reusable n8n workflow templates for common AI/automation scenarios
**Format**: JSON workflow definitions (importable into n8n)
**Count**: 2 workflow templates
**Focus Areas**: AI prompt engineering, semantic caching, cost optimization

### What is n8n?

n8n is a fair-code workflow automation platform that connects various services and APIs through visual workflow design. These templates can be imported directly into any n8n instance (cloud or self-hosted).

---

## Workflow Catalog

### 1. **Prompt Generator** 🚀
**File**: `prompt-generator.json` (554 lines, 32 KB)

An intelligent automation that generates high-quality, structured prompts for downstream AI agents using a multi-stage form collection and iterative refinement process.

#### Key Features
- **Multi-step form collection**: Gathers user intent, available tools, input/output specifications
- **AI-powered question generation**: Uses Google Gemini to generate 3 clarifying questions
- **Iterative refinement**: Loops through collecting user answers to specific questions
- **Structured prompt output**: Generates complete prompts following standardized format
- **Professional UI**: Custom CSS styling for polished user experience

#### Technology Stack
- **LLM**: Google Gemini (models/gemini-2.0-flash)
- **Framework**: n8n LangChain integration
- **Node Count**: 21 nodes (forms, AI chains, parsers, merge nodes)

#### Workflow Flow
```
On form submission
  ↓
BaseQuestions (collect: what to build, tools, input, output)
  ↓
RelatedQuestionAI (generates 3 clarifying questions)
  ↓
SplitQuestions & LoopQuestions (iterate through questions)
  ↓
RelevantQuestions (collect answers)
  ↓
MergeUserIntent (combine all collected data)
  ↓
PromptGenerator (create final structured prompt)
  ↓
SendingPrompt (display completed prompt to user)
```

#### Output Format
The generated prompt includes six structured sections:
- **Constraints**: Rules and boundaries for the AI agent
- **Role**: Agent expertise, persona, and purpose
- **Inputs**: Expected data format with examples
- **Tools**: Available resources and capabilities
- **Instructions**: Step-by-step procedures
- **Conclusions**: Expected output format and structure

#### Use Cases
- Creating consistent, professional AI prompts following best practices
- Building system prompts for downstream AI agents
- Iteratively refining prompts through guided questions
- Teams standardizing prompt engineering workflows
- Reducing prompt engineering trial-and-error time

#### Required Credentials
- Google Gemini API key (configured in n8n as credential)

---

### 2. **Semantic Cache with Redis Vector Store**
**File**: `semantic-cache-redis-vector-store.json` (452 lines, 14 KB)

Implements an intelligent semantic caching system that reduces LLM costs and improves response times by caching similar queries using vector similarity search.

#### Key Features
- **Semantic similarity search**: Uses Redis vector store to find similar previous queries
- **Dual-path processing**: Cache hit path (instant) vs. cache miss path (LLM call)
- **Cost optimization**: Configurable similarity threshold for precision/recall balance
- **Conversation memory**: Maintains context across interactions with Redis Chat Memory
- **Embedding-based matching**: Uses HuggingFace embeddings for semantic comparison

#### Technology Stack
- **LLM**: OpenAI GPT-4.1-mini
- **Vector Store**: Redis 8.x with vector search capability
- **Embeddings**: HuggingFace Inference API
- **Framework**: n8n LangChain integration
- **Interface**: n8n chat trigger and response nodes
- **Node Count**: 18 nodes (vector search, caching logic, LLM processing)

#### Workflow Flow
```
When chat message received
  ↓
Check for similar prompts (Redis vector search)
  ↓
Analyze results from store (filter by similarity threshold)
  ↓
Is this a cache hit? (decision node)
  ├─→ Cache Hit: Respond from semantic cache → return immediately
  └─→ Cache Miss: LLM Agent (generate new response)
      ↓
      Add response as metadata
      ↓
      Store entry in cache (save for future use)
      ↓
      Respond from LLM → return LLM response
```

#### Benefits
- **Faster responses**: Instant returns for cache hits (no LLM latency)
- **Cost reduction**: Skip expensive LLM API calls for similar queries
- **Configurable accuracy**: Adjust similarity threshold based on use case
- **Context preservation**: Conversation memory maintains chat history
- **Scalable**: Redis vector store handles large cache volumes

#### Use Cases
- Chat applications with repeated or similar queries
- Customer support chatbots with common questions
- Documentation Q&A systems
- Any LLM application needing cost optimization
- Systems requiring fast response times

#### Required Infrastructure
- Redis 8.x server with vector search enabled
- OpenAI API key
- HuggingFace Inference API key
- n8n instance with chat capabilities

---

## File Naming Convention

**Pattern**: `{workflow-type}-{descriptive-name}.json`

Examples:
- `prompt-generator.json` - Descriptive, hyphen-separated
- `semantic-cache-redis-vector-store.json` - Includes technology stack in name

**Unlike code snippets** in other folders:
- No hierarchical domain-category-subcategory pattern
- Technology-focused naming (redis, vector-store)
- Emphasizes workflow purpose over categorization

---

## How to Use These Workflows

### Prerequisites

1. **n8n Installation**
   - Self-hosted: [n8n.io/docs/hosting](https://n8n.io/docs/hosting)
   - Cloud: [n8n.io/cloud](https://n8n.io/cloud)

2. **Required Credentials**
   - For **Prompt Generator**: Google Gemini API key
   - For **Semantic Cache**: OpenAI API key, HuggingFace API key, Redis connection

3. **Infrastructure** (Semantic Cache only)
   - Redis 8.x server with vector search capability
   - Can use Redis Cloud, Redis Stack, or self-hosted Redis with RediSearch module

### Import Process

1. **Open n8n**: Navigate to your n8n instance
2. **Import Workflow**:
   - Click "Add workflow" → "Import from File"
   - Select the JSON file (`prompt-generator.json` or `semantic-cache-redis-vector-store.json`)
3. **Configure Credentials**:
   - Add API keys for required services
   - Update credential references in workflow nodes
4. **Customize Settings** (optional):
   - Adjust similarity thresholds
   - Modify form fields
   - Update LLM models or parameters
5. **Activate Workflow**: Toggle the workflow to "Active" state
6. **Test**: Use the provided test/trigger mechanisms

### Configuration Tips

#### Prompt Generator
- **Form customization**: Edit form nodes to collect domain-specific information
- **Model selection**: Can swap Google Gemini for other LLMs (OpenAI, Anthropic Claude)
- **Question count**: Adjust number of clarifying questions in `RelatedQuestionAI` node
- **Prompt template**: Modify final prompt structure in `PromptGenerator` node

#### Semantic Cache
- **Similarity threshold**: Default is 0.8 (80% similarity). Adjust in `Analyze results from store` node:
  - Higher (0.9-1.0): More precise, fewer false positives, lower cache hit rate
  - Lower (0.6-0.8): More lenient, higher cache hit rate, may return less relevant results
- **Cache TTL**: Configure Redis key expiration for automatic cache cleanup
- **Embedding model**: Can swap HuggingFace embeddings for OpenAI embeddings
- **LLM model**: Easily change GPT-4.1-mini to other models based on cost/quality needs

---

## Node Types Reference

### Common Node Categories Used

#### AI & Language Model Nodes
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini` - Google Gemini LLM
- `@n8n/n8n-nodes-langchain.lmChatOpenAi` - OpenAI GPT models
- `@n8n/n8n-nodes-langchain.agent` - Autonomous LLM agents
- `@n8n/n8n-nodes-langchain.chainLlm` - Structured LLM chains

#### Vector & Memory Nodes
- `@n8n/n8n-nodes-langchain.vectorStoreRedis` - Redis vector store
- `@n8n/n8n-nodes-langchain.memoryRedisChat` - Conversation memory
- `@n8n/n8n-nodes-langchain.embeddingsHuggingFaceInference` - Text embeddings

#### Form & UI Nodes
- `n8n-nodes-base.formTrigger` - Form submission trigger
- `n8n-nodes-base.form` - Interactive data collection forms
- `@n8n/n8n-nodes-langchain.chatTrigger` - Chat message trigger
- `@n8n/n8n-nodes-langchain.chat` - Chat response nodes

#### Processing & Logic Nodes
- `@n8n/n8n-nodes-langchain.outputParserStructured` - JSON output parsing
- `@n8n/n8n-nodes-langchain.outputParserAutofixing` - Auto-corrects malformed output
- `n8n-nodes-base.splitInBatches` - Array iteration
- `n8n-nodes-base.merge` - Data combination
- `n8n-nodes-base.if` - Conditional logic
- `n8n-nodes-base.code` - Custom JavaScript execution

---

## Architecture Patterns Demonstrated

### 1. **Multi-Stage Data Collection Pattern** (Prompt Generator)
**Problem**: Collecting complex, structured information from users
**Solution**: Progressive form disclosure with AI-guided question generation

**Benefits**:
- Reduces cognitive load (one question at a time)
- AI generates contextually relevant questions
- Ensures complete information gathering
- Better user experience than monolithic forms

**Pattern**:
```
Initial Form → AI Analysis → Generate Questions → Loop Through Questions → Final Synthesis
```

### 2. **Semantic Caching Pattern** (Semantic Cache)
**Problem**: High LLM API costs and latency for repeated queries
**Solution**: Vector similarity search to find semantically similar previous responses

**Benefits**:
- 10-100x cost reduction for cache hits
- Instant response times (no LLM latency)
- Handles query variations (not just exact matches)
- Scalable with vector databases

**Pattern**:
```
Query → Embed → Vector Search → Similarity Check → Return Cached or Generate New → Cache Result
```

### 3. **Structured Output Parsing Pattern** (Both Workflows)
**Problem**: LLMs produce unstructured text, need JSON/structured data
**Solution**: Output parsers with auto-fixing for malformed responses

**Benefits**:
- Reliable structured data from LLMs
- Automatic correction of common formatting errors
- Type-safe downstream processing
- Reduced post-processing complexity

### 4. **Conversation Memory Pattern** (Semantic Cache)
**Problem**: Chatbots need context from previous messages
**Solution**: Redis-backed chat memory preserves conversation history

**Benefits**:
- Stateful conversations across sessions
- Persistent storage (survives restarts)
- Efficient retrieval (Redis speed)
- Configurable context window

---

## Advanced Use Cases

### Extending the Prompt Generator

**1. Domain-Specific Prompts**
- Customize `BaseQuestions` form for specific domains (coding, writing, analysis)
- Add domain-specific constraints in the prompt template
- Include industry-specific best practices

**2. Multi-Language Support**
- Add language selection to initial form
- Translate questions and prompts using LLM
- Generate prompts in user's preferred language

**3. Prompt Library**
- Store generated prompts in a database (add Database node)
- Create search/retrieval system for previous prompts
- Build collaborative prompt repository

### Extending the Semantic Cache

**1. Hybrid Caching**
- Combine semantic cache with exact-match cache (Redis keys)
- Layer caching strategies (L1: exact, L2: semantic)
- Balance speed vs. accuracy

**2. Cache Analytics**
- Track cache hit rates (add Analytics node)
- Monitor cost savings (calculate avoided LLM calls)
- Identify common query patterns

**3. Multi-Tenant Caching**
- Add user/tenant ID to cache keys
- Isolate caches per customer
- Implement cache quotas

**4. Active Learning**
- Flag low-confidence cache hits for human review
- Retrain embeddings on corrected responses
- Continuously improve cache quality

---

## Performance Considerations

### Prompt Generator
- **Latency**: 10-30 seconds total (depends on number of clarifying questions)
- **Cost**: ~2-4 Gemini API calls per prompt generation
- **Scalability**: Form-based, scales with n8n instance capacity
- **Optimization**: Can reduce questions for faster generation

### Semantic Cache
- **Cache Hit**: <100ms (Redis query + response)
- **Cache Miss**: 1-5 seconds (LLM generation + embedding + storage)
- **Cost Savings**: 90%+ for high cache hit rates
- **Redis Requirements**:
  - Memory: ~1-10 MB per 1000 cached queries (depends on response length)
  - Vector index: RediSearch module required
- **Optimization**:
  - Tune similarity threshold based on use case
  - Implement cache expiration for stale data
  - Use Redis clustering for high-volume scenarios

---

## Security & Best Practices

### Credential Management
- **Never commit API keys**: Use n8n credential storage
- **Environment-specific credentials**: Separate dev/staging/prod keys
- **Rotate regularly**: Update API keys per security policy
- **Least privilege**: Use read-only or limited-scope API keys where possible

### Data Privacy
- **PII handling**: Be cautious caching user data in Redis
- **GDPR compliance**: Implement cache expiration and deletion mechanisms
- **Audit logs**: Track what queries are cached and by whom
- **Encryption**: Use Redis encryption-at-rest for sensitive data

### Error Handling
- **Graceful degradation**: Semantic cache falls back to LLM on cache errors
- **Retry logic**: Both workflows include error handling for API failures
- **Monitoring**: Add error notification nodes for production use
- **Timeout handling**: Configure appropriate timeouts for LLM calls

### Testing
- **Test mode**: Use n8n's test execution before activating
- **Sample data**: Validate with representative inputs
- **Edge cases**: Test with empty inputs, malformed data, API failures
- **Load testing**: Verify Redis can handle expected query volume

---

## Troubleshooting

### Common Issues

#### Prompt Generator
**Problem**: Forms not rendering
**Solution**: Check n8n webhook URL configuration and CORS settings

**Problem**: AI generates irrelevant questions
**Solution**: Improve context in `BaseQuestions` form, provide clearer examples

**Problem**: Structured output parsing fails
**Solution**: Enable auto-fixing parser, or adjust output schema

#### Semantic Cache
**Problem**: Redis connection errors
**Solution**: Verify Redis server is running, check connection string and credentials

**Problem**: Low cache hit rate
**Solution**: Lower similarity threshold, verify embeddings are consistent

**Problem**: Cached responses are stale
**Solution**: Implement cache TTL (time-to-live) or manual cache invalidation

**Problem**: Vector search is slow
**Solution**: Ensure RediSearch indexes are created, optimize index parameters

---

## Version History

### Current Version
- **Date Added**: November 22, 2025 (Commit 2dfb199)
- **Author**: Kyle Jovanovic
- **n8n Version**: Compatible with n8n 1.0+
- **LangChain Nodes**: @n8n/n8n-nodes-langchain latest

### Dependencies
- **n8n**: 1.0 or higher
- **Redis**: 8.x with RediSearch module (for semantic cache)
- **LangChain**: n8n LangChain integration nodes
- **APIs**: Google Gemini, OpenAI, HuggingFace Inference

---

## Related Resources

### n8n Documentation
- [n8n Workflows Documentation](https://docs.n8n.io/workflows/)
- [n8n LangChain Integration](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain/)
- [n8n Community Workflows](https://n8n.io/workflows/)

### External Services
- [Google Gemini API](https://ai.google.dev/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [HuggingFace Inference API](https://huggingface.co/inference-api)
- [Redis Vector Search](https://redis.io/docs/stack/search/reference/vectors/)

### Related Repository Content
- **Data Engineering**: See `Data-Engineering/` for data pipeline patterns
- **ML Ops**: See `ML-Ops/` for model serving and monitoring examples
- **Code Snippets**: Unlike Workflows, other folders contain self-contained Python code

---

## Contributing

### Adding New Workflows

When contributing new workflow templates:

1. **Naming Convention**: Use descriptive, hyphen-separated names
   - Format: `{workflow-type}-{descriptive-name}.json`
   - Example: `data-enrichment-with-multiple-apis.json`

2. **Documentation**: Include in-workflow documentation
   - Add Sticky Notes explaining workflow sections
   - Document key configuration parameters
   - Provide usage examples

3. **Update README**: Add new workflow to this catalog
   - Follow existing template structure
   - Include: Features, Tech Stack, Use Cases, Prerequisites

4. **Testing**: Verify workflow before committing
   - Test in n8n instance
   - Validate all credential references work
   - Include sample test data or instructions

5. **Credentials**: Never commit actual API keys
   - Use credential references only
   - Document required credential types
   - Provide setup instructions

---

## Quick Reference

### File Inventory
```
Workflows/
├── README.md (this file)
├── prompt-generator.json (554 lines) - AI prompt generation workflow
└── semantic-cache-redis-vector-store.json (452 lines) - Semantic caching system
```

### When to Use Each Workflow

**Use Prompt Generator when:**
- Building AI agents and need consistent prompt formatting
- Iteratively refining prompts through user feedback
- Creating system prompts for downstream applications
- Standardizing prompt engineering across a team

**Use Semantic Cache when:**
- Reducing LLM API costs for production chat applications
- Improving response times for common queries
- Building customer support chatbots with repeated questions
- Implementing FAQ systems with semantic matching

---

## Summary

The **Workflows** folder provides production-ready n8n automation templates that complement the code snippet collection in this repository. While other folders contain self-contained Python code demonstrating best practices, this folder offers complete, runnable workflow automations for common AI/automation scenarios.

**Key Differentiators**:
- **Format**: JSON workflow definitions (not Python code)
- **Execution**: Requires n8n platform (not standalone scripts)
- **Integration**: Connects multiple services via visual workflows
- **Purpose**: End-to-end automation (not reference implementations)
- **Dependencies**: External services and APIs (not just Python libraries)

These workflows demonstrate advanced patterns in AI automation, cost optimization, and user experience design, making them valuable learning resources and production starting points.
