from gradio.context import Context


class BlockManager:
    def __init__(self, block):
        self.block = block

    def __enter__(self):
        self.previous_block = Context.block
        Context.block = self.block
        return self

    def __exit__(self, *args, **kwargs):
        Context.block = self.previous_block


class ParentBlock(BlockManager):
    def __init__(self):
        super().__init__(Context.block.parent)
