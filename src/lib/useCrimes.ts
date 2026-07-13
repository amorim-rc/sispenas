import {useEffect, useState} from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';
import type {Crime} from './types';

export interface CrimesState {
  crimes: Crime[];
  loading: boolean;
  error: string | null;
}

export function useCrimes(): CrimesState {
  const url = useBaseUrl('/data/crimes.json');
  const [state, setState] = useState<CrimesState>({crimes: [], loading: true, error: null});

  useEffect(() => {
    let active = true;
    fetch(url)
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((data: Crime[]) => {
        if (active) setState({crimes: data, loading: false, error: null});
      })
      .catch((e: Error) => {
        if (active) setState({crimes: [], loading: false, error: e.message});
      });
    return () => {
      active = false;
    };
  }, [url]);

  return state;
}
