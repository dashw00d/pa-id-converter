mzones = ['Front Door',
          'Front',
          'Back',
          'Dining Room Window',
          'R',
          'Y',
          'A',
          'N']


class ZoneNames:

    def convert(self, input):
        self.input = input
        lines = self.input.split()
        final = []
        for l in lines:

            if l in mzones:
                self.input = 'success'
                final.append(l)
                final.append('  ')
            final.append('\n')

        ''.join(final)
        return final
