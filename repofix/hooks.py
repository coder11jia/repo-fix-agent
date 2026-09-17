from agents import RunHooks


class RepoFixHooks(RunHooks):

    async def on_agent_start(
        self,
        context,
        agent,
    ):
        print(
            f"\n[Agent] {agent.name} started"
        )

    async def on_tool_start(
        self,
        context,
        agent,
        tool,
    ):
        tool_name = getattr(
            tool,
            "name",
            tool.__class__.__name__,
        )

        print(
            f"  → Tool: {tool_name}"
        )

    async def on_tool_end(
        self,
        context,
        agent,
        tool,
        result,
    ):
        tool_name = getattr(
            tool,
            "name",
            tool.__class__.__name__,
        )

        print(
            f"  ✓ Tool: {tool_name}"
        )

    async def on_agent_end(
        self,
        context,
        agent,
        output,
    ):
        usage = context.usage

        print()
        print(
            f"[Agent] Finished | "
            f"LLM requests: {usage.requests} | "
            f"Tokens: {usage.total_tokens}"
        )