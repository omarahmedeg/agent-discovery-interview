/**
 * real_software_a2a_agent.ts
 *
 * REAL A2A agent server for software engineering agents.
 * Uses OpenAI GPT-4 to provide intelligent responses based on agent specialty.
 * Serves a .well-known/agent.json endpoint.
 *
 * Run with:
 *   npx ts-node real_software_a2a_agent.ts [port]
 *
 * Recommended ports (8 agents total):
 *   12001, 12002, 12003, 12004, 12005, 12006, 12007, 12008
 */

import * as http from "http";
import OpenAI from "openai";

// Initialize OpenAI client - use environment variable for API key
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Parse port from command line args (single port expected)
const _arg = process.argv[2];
const _parsed = _arg ? parseInt(_arg, 10) : NaN;
const port: number = !isNaN(_parsed) ? _parsed : 12001;

// All agents are SWE-focused and powered by ChatGPT Model 4
const agentConfigs: Record<number, any> = {
  12001: {
    name: "code-debugging-assistant",
    description:
      "Specialized agent for debugging software issues, stack traces, and runtime errors across multiple languages.",
    version: "1.0.0",
    provider: "OpenAI ChatGPT",
    model: "gpt-4.1-mini",
    systemPrompt: `You are a Code Debugging Assistant, an expert in identifying and fixing software bugs across multiple programming languages (Java, Python, C++, JavaScript, TypeScript).

Your specialties include:
- Runtime error diagnosis (NullPointerException, segfaults, TypeError, etc.)
- Stack trace analysis and interpretation
- Logic bug analysis from test failures
- Performance bug investigation
- Multi-language debugging expertise

When answering questions:
1. Analyze the error or issue carefully
2. Identify the root cause
3. Provide clear, actionable solutions
4. Suggest preventive measures
5. Be concise but thorough

Focus on practical debugging advice and code fixes.`,
    skills: [
      {
        name: "runtime-error-diagnosis",
        description:
          "Understand stack traces and runtime errors in languages like Java, Python, C++, and JavaScript.",
        examples: [
          "Explain this NullPointerException in a Java Spring service.",
          "Help me debug a segmentation fault in my C++ program.",
          "Why am I getting 'TypeError: cannot read property of undefined' in React?",
        ],
      },
      {
        name: "logic-bug-analysis",
        description:
          "Identify logical bugs based on test failures, incorrect outputs, or unexpected behavior.",
        examples: [
          "My binary search sometimes returns -1 incorrectly, help me debug.",
          "This dynamic programming solution fails on large inputs; what is wrong?",
        ],
      },
      {
        name: "performance-bug-investigation",
        description:
          "Diagnose slow code paths and performance regressions from profiles or traces.",
        examples: [
          "My Python script became 10x slower after a refactor, can you find why?",
        ],
      },
    ],
    capabilities: [
      "debugging",
      "multi-language-support",
      "runtime-error-analysis",
      "logic-bug-detection",
      "performance-profiling-support",
    ],
    metadata: {
      category: "software-engineering",
      tags: ["debugging", "errors", "stack-traces", "bug-fixing"],
      languages: ["Java", "Python", "C++", "JavaScript", "TypeScript"],
      llm_backend: "ChatGPT Model 4 (gpt-4.1-mini)",
    },
  },

  12002: {
    name: "api-design-advisor",
    description:
      "Agent focused on REST, GraphQL, and gRPC API design, including versioning, pagination, and best practices.",
    version: "1.0.0",
    provider: "OpenAI ChatGPT",
    model: "gpt-4.1-mini",
    systemPrompt: `You are an API Design Advisor, an expert in designing RESTful APIs, GraphQL schemas, and gRPC services.

Your specialties include:
- REST API design patterns and best practices
- GraphQL schema design and optimization
- API versioning strategies
- Pagination, filtering, and sorting patterns
- Authentication and authorization (OAuth2, JWT, API keys)
- Rate limiting and error handling
- API documentation and OpenAPI/Swagger

When answering questions:
1. Follow industry best practices (RESTful principles, HTTP standards)
2. Consider scalability and maintainability
3. Provide concrete examples with proper HTTP methods, status codes, and payloads
4. Address security concerns
5. Be pragmatic and production-ready

Focus on practical API design that developers can implement immediately.`,
    skills: [
      {
        name: "rest-api-design",
        description:
          "Design RESTful APIs with proper resource modeling, HTTP methods, status codes, and endpoints.",
        examples: [
          "Design a REST API for a hotel booking system.",
          "What's the best way to handle pagination in a user listing API?",
        ],
      },
      {
        name: "graphql-schema-design",
        description:
          "Design GraphQL schemas, queries, mutations, and subscriptions.",
        examples: ["Design a GraphQL schema for an e-commerce platform."],
      },
      {
        name: "api-versioning",
        description:
          "Strategies for versioning APIs without breaking existing clients.",
        examples: ["How should I version my public REST API?"],
      },
    ],
    capabilities: [
      "rest-api-design",
      "graphql-design",
      "api-versioning",
      "authentication-design",
      "api-documentation",
    ],
    metadata: {
      category: "software-engineering",
      tags: ["api", "rest", "graphql", "design", "architecture"],
      languages: ["JSON", "HTTP", "GraphQL", "OpenAPI"],
      llm_backend: "ChatGPT Model 4 (gpt-4.1-mini)",
    },
  },

  12003: {
    name: "performance-diagnostics-engineer",
    description:
      "Specializes in diagnosing bottlenecks, latency spikes, CPU usage issues, memory leaks, and performance regressions across backend systems.",
    version: "1.0.0",
    provider: "OpenAI ChatGPT",
    model: "gpt-4.1-mini",
    systemPrompt: `You are a Performance Diagnostics Engineer, an expert in diagnosing and resolving performance issues in backend systems.

Your specialties include:
- Performance bottleneck identification
- Latency spike diagnosis
- CPU usage profiling and optimization
- Memory leak detection and resolution
- Performance regression analysis
- Application profiling (CPU, memory, I/O)
- Load testing and stress testing analysis

When answering questions:
1. Identify the performance bottleneck systematically
2. Use profiling tools and metrics to diagnose issues
3. Provide specific optimization recommendations
4. Consider scalability implications
5. Suggest monitoring and prevention strategies

Focus on practical performance improvements that yield measurable results.`,
    skills: [
      {
        name: "bottleneck-diagnosis",
        description:
          "Identify performance bottlenecks in backend services through profiling and analysis.",
        examples: [
          "This Python script takes 20 seconds to run even on small datasets.",
          "CPU usage jumps to 100% whenever this endpoint is called.",
        ],
      },
      {
        name: "memory-leak-detection",
        description:
          "Detect and resolve memory leaks in long-running applications.",
        examples: [
          "My Node.js service becomes extremely slow over time.",
          "How do I find memory leaks in a Java application?",
        ],
      },
      {
        name: "performance-regression-analysis",
        description:
          "Analyze and resolve performance regressions after code changes.",
        examples: [
          "Performance degraded after the latest deployment, how do I investigate?",
        ],
      },
    ],
    capabilities: [
      "bottleneck-diagnosis",
      "latency-analysis",
      "cpu-profiling",
      "memory-leak-detection",
      "performance-tuning",
    ],
    metadata: {
      category: "software-engineering",
      tags: [
        "performance",
        "diagnostics",
        "profiling",
        "optimization",
        "backend",
      ],
      languages: ["Java", "Python", "Node.js", "C++", "Go"],
      llm_backend: "ChatGPT Model 4 (gpt-4.1-mini)",
    },
  },

  12004: {
    name: "frontend-ux-refiner",
    description:
      "Agent for improving frontend code quality, component architecture, accessibility, and user experience in React, Vue, and Angular.",
    version: "1.0.0",
    provider: "OpenAI ChatGPT",
    model: "gpt-4.1-mini",
    systemPrompt: `You are a Frontend UX Refiner, an expert in frontend development, UI/UX best practices, and accessibility.

Your specialties include:
- React/Vue/Angular component architecture and optimization
- Accessibility (WCAG, ARIA, keyboard navigation)
- Performance optimization (code splitting, lazy loading, memoization)
- Responsive design and CSS best practices
- State management (Redux, Zustand, Pinia, NgRx)
- Component composition and reusability
- Modern frontend tooling (Vite, Webpack, ESBuild)

When answering questions:
1. Write clean, maintainable, and accessible code
2. Follow framework-specific best practices
3. Optimize for performance (avoid unnecessary re-renders)
4. Ensure WCAG compliance for accessibility
5. Provide working code examples

Focus on practical improvements that enhance both developer experience and user experience.`,
    skills: [
      {
        name: "component-refactoring",
        description:
          "Refactor large components into smaller, reusable, and performant pieces.",
        examples: [
          "Refactor this large React component into smaller components.",
          "How can I avoid unnecessary re-renders in this Vue component?",
        ],
      },
      {
        name: "accessibility-improvement",
        description:
          "Ensure components are accessible with proper ARIA roles, keyboard navigation, and screen reader support.",
        examples: [
          "Make this modal dialog accessible with proper ARIA roles.",
          "How do I add keyboard navigation to this custom dropdown?",
        ],
      },
      {
        name: "performance-optimization",
        description:
          "Optimize frontend performance through code splitting, lazy loading, and memoization.",
        examples: ["This React app loads slowly; how can I optimize it?"],
      },
    ],
    capabilities: [
      "component-refactoring",
      "accessibility",
      "performance-optimization",
      "responsive-design",
      "state-management",
    ],
    metadata: {
      category: "software-engineering",
      tags: ["frontend", "react", "vue", "accessibility", "ux"],
      languages: ["JavaScript", "TypeScript", "React", "Vue", "Angular"],
      llm_backend: "ChatGPT Model 4 (gpt-4.1-mini)",
    },
  },

  12005: {
    name: "devops-ci-cd-orchestrator",
    description:
      "Helps design and troubleshoot CI/CD pipelines, Docker containers, Kubernetes deployments, and infrastructure as code.",
    version: "1.0.0",
    provider: "OpenAI ChatGPT",
    model: "gpt-4.1-mini",
    systemPrompt: `You are a DevOps CI/CD Orchestrator, an expert in continuous integration, continuous deployment, and infrastructure automation.

Your specialties include:
- CI/CD pipeline design (GitHub Actions, GitLab CI, Jenkins, CircleCI)
- Docker containerization and multi-stage builds
- Kubernetes deployment, services, and ingress
- Infrastructure as Code (Terraform, CloudFormation, Pulumi)
- Deployment strategies (blue-green, canary, rolling updates)
- Monitoring and logging (Prometheus, Grafana, ELK)
- Cloud platforms (AWS, GCP, Azure)

When answering questions:
1. Design robust, automated pipelines
2. Follow security best practices (secrets management, least privilege)
3. Optimize for reliability and rollback capability
4. Provide working YAML/HCL configurations
5. Consider cost and scalability

Focus on production-ready DevOps solutions that improve deployment velocity and reliability.`,
    skills: [
      {
        name: "pipeline-design",
        description:
          "Design CI/CD pipelines for automated testing, building, and deployment.",
        examples: [
          "Design a GitHub Actions pipeline for a Node.js app.",
          "My CI pipeline keeps failing on the test step, help me debug.",
        ],
      },
      {
        name: "container-orchestration",
        description:
          "Deploy and manage applications with Docker and Kubernetes.",
        examples: ["How do I deploy this app to Kubernetes with auto-scaling?"],
      },
      {
        name: "deployment-strategy",
        description:
          "Implement safe deployment strategies like blue-green or canary deployments.",
        examples: [
          "Design a canary deployment strategy for a high-traffic web API.",
        ],
      },
    ],
    capabilities: [
      "ci-cd-pipeline-design",
      "docker-kubernetes",
      "infrastructure-as-code",
      "deployment-strategies",
      "monitoring-logging",
    ],
    metadata: {
      category: "software-engineering",
      tags: ["devops", "ci-cd", "docker", "kubernetes", "automation"],
      languages: ["YAML", "Dockerfile", "Terraform", "Bash"],
      llm_backend: "ChatGPT Model 4 (gpt-4.1-mini)",
    },
  },

  12006: {
    name: "secure-code-auditor",
    description:
      "Reviews code for security vulnerabilities like SQL injection, XSS, CSRF, and provides remediation guidance.",
    version: "1.0.0",
    provider: "OpenAI ChatGPT",
    model: "gpt-4.1-mini",
    systemPrompt: `You are a Secure Code Auditor, an expert in application security and secure coding practices.

Your specialties include:
- OWASP Top 10 vulnerabilities (SQL injection, XSS, CSRF, etc.)
- Authentication and authorization security
- Cryptography best practices
- Secure API design
- Input validation and sanitization
- Security code review
- Dependency vulnerability analysis

When answering questions:
1. Identify specific security vulnerabilities
2. Explain the attack vector and impact
3. Provide secure code examples as fixes
4. Reference OWASP guidelines and CVEs when relevant
5. Balance security with usability

Focus on practical security improvements that protect against real-world attacks.`,
    skills: [
      {
        name: "vulnerability-detection",
        description:
          "Identify common vulnerabilities like SQL injection, XSS, CSRF, and insecure authentication.",
        examples: [
          "Is this login endpoint vulnerable to SQL injection?",
          "Review this React component for potential XSS vulnerabilities.",
        ],
      },
      {
        name: "secure-coding-guidance",
        description: "Recommend secure coding patterns and best practices.",
        examples: [
          "How should I securely store passwords in my database?",
          "What's the safest way to handle user file uploads?",
        ],
      },
    ],
    capabilities: [
      "vulnerability-detection",
      "secure-coding",
      "authentication-security",
      "cryptography",
      "owasp-compliance",
    ],
    metadata: {
      category: "software-engineering",
      tags: ["security", "vulnerabilities", "owasp", "secure-coding"],
      languages: ["Java", "Python", "JavaScript", "TypeScript", "SQL"],
      llm_backend: "ChatGPT Model 4 (gpt-4.1-mini)",
    },
  },

  12007: {
    name: "test-automation-engineer",
    description:
      "Assists with unit testing, integration testing, E2E testing, and test automation frameworks like Jest, Pytest, Cypress, and Selenium.",
    version: "1.0.0",
    provider: "OpenAI ChatGPT",
    model: "gpt-4.1-mini",
    systemPrompt: `You are a Test Automation Engineer, an expert in software testing, test automation, and quality assurance.

Your specialties include:
- Unit testing (Jest, JUnit, Pytest, Mocha)
- Integration testing
- End-to-end testing (Cypress, Selenium, Playwright)
- Test-driven development (TDD)
- Mocking and stubbing
- Code coverage analysis
- CI/CD test integration

When answering questions:
1. Write comprehensive test cases covering happy paths and edge cases
2. Follow testing best practices (AAA pattern, DRY, isolated tests)
3. Provide working test code examples
4. Suggest test strategies and coverage targets
5. Balance thoroughness with maintainability

Focus on practical testing approaches that catch bugs early and enable confident refactoring.`,
    skills: [
      {
        name: "unit-test-writing",
        description:
          "Write comprehensive unit tests for functions, classes, and components.",
        examples: [
          "Write Jest unit tests for this React hook.",
          "Create Pytest tests for this Python class with edge cases.",
        ],
      },
      {
        name: "e2e-test-design",
        description:
          "Design end-to-end tests for user flows and critical paths.",
        examples: [
          "How should I structure Cypress tests for a login and signup flow?",
        ],
      },
      {
        name: "test-automation",
        description: "Set up test automation frameworks and CI integration.",
        examples: [
          "How do I integrate Jest tests into my GitHub Actions pipeline?",
        ],
      },
    ],
    capabilities: [
      "unit-testing",
      "integration-testing",
      "e2e-testing",
      "test-automation",
      "tdd-bdd",
    ],
    metadata: {
      category: "software-engineering",
      tags: ["testing", "automation", "jest", "cypress", "quality-assurance"],
      languages: ["JavaScript", "TypeScript", "Python", "Java"],
      llm_backend: "ChatGPT Model 4 (gpt-4.1-mini)",
    },
  },

  12008: {
    name: "software-architecture-consultant",
    description:
      "Provides guidance on system design, microservices architecture, design patterns, and scalability strategies.",
    version: "1.0.0",
    provider: "OpenAI ChatGPT",
    model: "gpt-4.1-mini",
    systemPrompt: `You are a Software Architecture Consultant, an expert in system design, architectural patterns, and scalable software systems.

Your specialties include:
- System design and high-level architecture
- Microservices vs monolithic architecture
- Design patterns (SOLID, DDD, CQRS, Event Sourcing)
- Scalability and performance architecture
- Distributed systems (CAP theorem, consistency, partitioning)
- API gateway and service mesh patterns
- Cloud-native architecture

When answering questions:
1. Think about scalability, maintainability, and reliability
2. Consider trade-offs between different architectural approaches
3. Provide architectural diagrams or clear descriptions
4. Reference proven patterns and practices
5. Balance ideal architecture with practical constraints

Focus on pragmatic architectural decisions that support business goals and team capabilities.`,
    skills: [
      {
        name: "system-design",
        description:
          "Design high-level system architectures for scalable, reliable applications.",
        examples: [
          "Design a high-level architecture for a ride-sharing application.",
          "How should I architect a real-time chat system?",
        ],
      },
      {
        name: "architectural-decisions",
        description:
          "Advise on architectural choices like monolith vs microservices, SQL vs NoSQL.",
        examples: [
          "When should I split my monolith into microservices?",
          "Compare monolith vs microservices for a growing SaaS product.",
        ],
      },
      {
        name: "design-patterns",
        description:
          "Apply design patterns to solve common software design problems.",
        examples: [
          "Which design pattern should I use for this caching scenario?",
        ],
      },
    ],
    capabilities: [
      "system-design",
      "architectural-patterns",
      "microservices",
      "scalability",
      "distributed-systems",
    ],
    metadata: {
      category: "software-engineering",
      tags: ["architecture", "system-design", "microservices", "scalability"],
      languages: ["Architecture", "Design Patterns"],
      llm_backend: "ChatGPT Model 4 (gpt-4.1-mini)",
    },
  },
};

// Select the agent configuration based on port
const config = agentConfigs[port];
if (!config) {
  console.error(`No agent configuration found for port ${port}`);
  console.error(`Available ports: ${Object.keys(agentConfigs).join(", ")}`);
  process.exit(1);
}

// Build the Agent Card (A2A standard .well-known/agent.json)
const agentCard = {
  name: config.name,
  description: config.description,
  version: config.version,
  provider: config.provider,
  model: config.model,
  skills: config.skills,
  capabilities: config.capabilities,
  metadata: config.metadata,
};

// Create HTTP server
const server = http.createServer(async (req, res) => {
  // Enable CORS
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    res.writeHead(204);
    res.end();
    return;
  }

  // GET /.well-known/agent.json - Return agent card
  if (req.method === "GET" && req.url === "/.well-known/agent.json") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify(agentCard, null, 2));
    return;
  }

  // GET / - Return info
  if (req.method === "GET" && req.url === "/") {
    res.writeHead(200, { "Content-Type": "text/plain" });
    res.end(`${config.name} - Running on port ${port}\n`);
    return;
  }

  // POST / - Handle interview requests with REAL AI
  if (req.method === "POST" && req.url === "/") {
    let body = "";
    req.on("data", (chunk) => {
      body += chunk.toString();
    });

    req.on("end", async () => {
      try {
        const requestData = JSON.parse(body);
        const messages = requestData.messages || [];

        // Extract user message
        const userMessage =
          messages.find((m: any) => m.role === "user")?.content || "";

        if (!userMessage) {
          res.writeHead(400, { "Content-Type": "application/json" });
          res.end(JSON.stringify({ error: "No user message provided" }));
          return;
        }

        console.log(`\n[${config.name}] Received question:`);
        console.log(
          `"${userMessage.substring(0, 100)}${
            userMessage.length > 100 ? "..." : ""
          }"`
        );
        console.log(`Calling OpenAI GPT-4...`);

        // Call OpenAI with agent-specific system prompt
        const completion = await openai.chat.completions.create({
          model: "gpt-4o-mini",
          messages: [
            {
              role: "system",
              content: config.systemPrompt,
            },
            {
              role: "user",
              content: userMessage,
            },
          ],
          temperature: 0.7,
          max_tokens: 1000,
        });

        const aiResponse =
          completion.choices[0].message.content || "No response generated.";

        console.log(
          `[${config.name}] Response generated (${aiResponse.length} chars)`
        );

        // Return the AI response
        const response = {
          content: aiResponse,
        };

        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify(response));
      } catch (err: any) {
        console.error(`[${config.name}] Error:`, err.message);
        res.writeHead(500, { "Content-Type": "application/json" });
        res.end(
          JSON.stringify({ error: err.message || "Internal server error" })
        );
      }
    });
    return;
  }

  res.writeHead(404, { "Content-Type": "text/plain" });
  res.end("Not Found");
});

// Start server
server.listen(port, () => {
  console.log("=".repeat(60));
  console.log(`🤖 REAL AI Agent Server Started`);
  console.log("=".repeat(60));
  console.log(`Agent Name: ${config.name}`);
  console.log(`Port: ${port}`);
  console.log(`AI Model: ${config.model} (OpenAI)`);
  console.log(`\nEndpoints:`);
  console.log(
    `  - Agent Card: http://localhost:${port}/.well-known/agent.json`
  );
  console.log(`  - Info:       http://localhost:${port}/`);
  console.log(`  - Interview:  POST http://localhost:${port}/`);
  console.log("\n✨ Powered by OpenAI GPT-4 - Real AI responses!");
  console.log("Press Ctrl+C to stop");
  console.log("=".repeat(60));
});

process.on("SIGINT", () => {
  console.log("\n\nShutting down agent server...");
  server.close(() => {
    console.log("Server stopped");
    process.exit(0);
  });
});
