import typing as t

class Material:
    """ Material class which returns different type of material
    depending on the html code """
    
    ppc = ['polyacrylic', 'polyester', 'cotton']
    pp = ['polypropylene', 'polyester']
    pp100 = ['polypropylene', '100']
    pe100 = ['polyester', '100']
    cotton100 = ['cotton', '100']
    wc = ['wool', 'cotton']

    def __init__(self, html) -> None:
        self.html = html
        
    def get_material(self):
        if all(mat in self.html for mat in self.ppc):
            return self._combine(self._polyacrylic, self._cotton, self._polyester)
        elif all(mat in self.html for mat in self.pp):
            return self._combine(self._popypropylene, self._polyester)
        elif all(mat in self.html for mat in self.pp100):
            return self._combine(self._popypropylene)
        elif all(mat in self.html for mat in self.pe100):
            return self._combine(self._polyester)
        elif all(mat in self.html for mat in self.cotton100):
            return self._combine(self._cotton)
        elif all(mat in self.html for mat in self.wc):
            return self._combine(self._wool, self._cotton)
        else:
            return self._combine(self._popypropylene)

    def _combine(self, *args:t.Callable) -> str:
        outl = [arg() for arg in args]
        return '|'.join(outl)

    def _popypropylene(self) -> str:
        return 'Polypropylene/Olefin'

    def _polyester(self) -> str:
        return 'Polyester'

    def _polyacrylic(self) -> str:
        return 'Polyacrylic'

    def _cotton(self) -> str:
        return 'Cotton'

    def _wool(self) -> str:
        return 'Wool'