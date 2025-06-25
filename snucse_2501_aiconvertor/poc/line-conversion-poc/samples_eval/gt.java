
package am.im.securitiesinqrpritmgmt.service.impl;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import javax.annotation.Resource;

import org.springframework.stereotype.Service;

import am.im.securitiesinqrpritmgmt.service.SecuritiesInqrPritMgmtBCService;
import custom.cmmn.exception.CgAppUserException;
import custom.cmmn.util.MapDataUtil;
import custom.cmmn.util.UserHeaderUtil;
import com.inswave.elfw.exception.ElException;
import com.inswave.ext.cg.util.CodeUtil;


@Service("securitiesInqrPritMgmtBCServiceImpl")
public class SecuritiesInqrPritMgmtBCServiceImpl implements SecuritiesInqrPritMgmtBCService {

    
    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectInterestRtrvDuda(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0015(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectDepositsPsst(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0014(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectDepositsBalance(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0005(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectDepositsWithdrawal(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0004(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectGnrzReport(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0013(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectCdSalePsst(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0012(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectBondsSalePsst(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0011(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectOperatingFundsPsst(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0010(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectFundsExecution(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0009(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectExpirationPsst(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0008(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectMmtLedger(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        String trnsDateFrom = null;
        String trnsDateTo = null;
        try {
            
            
            trnsDateFrom = pDoc.getTrnsDateFrom();
            trnsDateTo = pDoc.getTrnsDateTo();
            pDoc.setTrnsDateFrom1(trnsDateFrom);
            pDoc.setTrnsDateTo1(trnsDateTo);
            pDoc.setTrnsDateFrom2(trnsDateFrom);
            pDoc.setTrnsDateTo2(trnsDateTo);
            pDoc.setEstbBankTrnsBrcd1(pDoc.getEstbBankTrnsBrcd());
            pDoc.setEstbBankTrnsBrcd2(pDoc.getEstbBankTrnsBrcd());
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0006(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectSecuritiesLedger(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0002(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectKsdDpstCdBondsPsst(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0001(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public SecuritiesInqrPritMgmtVo selectSecuritiesStrcPrdtInfo(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        SecuritiesInqrPritMgmtVo result = null;
        SecuritiesInqrPritMgmtVo bizInput = new SecuritiesInqrPritMgmtVo();
        ;
        ArrayList<SecuritiesInqrPritMgmtVo> bizOutput = null;
        String invtAvbl = "";
        Long frcrInvtAvbl = 0l;
        String spotEcrt = "";
        Double ecrtUnitVl = 0.0d;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0016(pDoc);
            
            bizOutput = comCgAmImSecuritiesmgmtImzscinvtdtlsDaoDAO.im_zsc_invt_dtls_so0003(pDoc);
            
            
            bizInput.setVectorBaln(bizOutput);
            
            
            
            bizInput.setCalcStda(result.getPurDate());
            
            bizInput.setCalcEnda(pDoc.getBsda());
            
            
            bizInput.setEndaPrevFlag("Y");
            
            bizOutput = null;
            invtAvbl = bizOutput.getInvtAvbl();
            spotEcrt = result.getSpotEcrt();
            ecrtUnitVl = result.getEcrtUnitVl();
            
            
            result.setInvtAvbl(invtAvbl);
            if (!spotEcrt.isEmpty()) {
                
                frcrInvtAvbl = Math.round(Double.parseDouble(invtAvbl) / Double.parseDouble(spotEcrt) * ecrtUnitVl);
                
                result.setFrcrInvtAvbl(String.valueOf(frcrInvtAvbl));
            }
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectSecuritiesStrcPrdtTrns(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0017(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public ArrayList<SecuritiesInqrPritMgmtVo> selectInvtReturnRate(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        ArrayList<SecuritiesInqrPritMgmtVo> result = null;
        try {
            
            
            result = comCgAmImSecuritiesinqrpritmgmtImzscprdtDaoDAO.im_zsc_prdt_so0018(pDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public SecuritiesInqrPritMgmtVo selectVldtDcntCondIntsPaynCond(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        SecuritiesInqrPritMgmtVo result = null;
        ArrayList<SecuritiesInqrPritMgmtVo> intsPaynCondCdDoc = null;
        ArrayList<SecuritiesInqrPritMgmtVo> vldtDcntCondCdDoc = null;
        try {
            result = new SecuritiesInqrPritMgmtVo();
            
            
            intsPaynCondCdDoc = comCgAmImSecuritiesinqrpritmgmtImzscintspayncondcdDaoDAO.im_zsc_ints_payn_cond_cd_so0001(pDoc);
            
            vldtDcntCondCdDoc = comCgAmImSecuritiesinqrpritmgmtImzscvldtdcntcondcdDaoDAO.im_zsc_vldt_dcnt_cond_cd_so0001(pDoc);
            
            result.setIntsPaynCondCdList(intsPaynCondCdDoc);
            
            result.setVldtDcntCondCdList(vldtDcntCondCdDoc);
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

    
    public SecuritiesInqrPritMgmtVo saveVldtDcntCondIntsPaynCond(SecuritiesInqrPritMgmtVo pDoc) throws ElException {
        SecuritiesInqrPritMgmtVo result = null;
        SecuritiesInqrPritMgmtVo intsPaynCondCdDoc = null;
        SecuritiesInqrPritMgmtVo vldtDcntCondCdDoc = null;
        SecuritiesInqrPritMgmtVo listInts = null;
        SecuritiesInqrPritMgmtVo listVldt = null;
        SecuritiesInqrPritMgmtVo resultInts = null;
        SecuritiesInqrPritMgmtVo resultVldt = null;
        String errCd = "";
        String errMsg = "";
        try {
            
            
            intsPaynCondCdDoc = /* 주석처리(as-is) XMLUtil.toXML(XMLUtil.getVector(pDoc, "INTS_PAYN_COND_CD_LIST"))*/;
            ArrayList aryListInts = /* 수동가이드 예정 (as-is) XMLUtil.toArrayList(intsPaynCondCdDoc)*/;
            Iterator<SecuritiesInqrPritMgmtVo> itrInts = aryListInts.iterator();
            
            while (itrInts.hasNext()) {
                listInts = itrInts.next();
                
                listInts.setLastChnrId((String) UserHeaderUtil.getInstance().getEmpno());
                
                listInts.setLastChngDttm((String) UserHeaderUtil.getInstance().getTimestamp());
                
                if (("3").equals(listInts.getStatus())) {
                    
                    resultInts = comCgAmImSecuritiesinqrpritmgmtImzscstrcintscondDaoDAO.im_zsc_strc_ints_cond_so0002(listInts);
                    if (resultInts.getCnt() > 0) {
                        errCd = "E00000";
                        errMsg = "현재 사용하고 있는 조건입니다.";
                        throw new CgAppUserException("CG_ERROR", 0, CodeUtil.getCodeValue("CGMsgCode", "E", errCd, new String[] { errMsg }), errCd);
                    }
                    comCgAmImSecuritiesinqrpritmgmtImzscintspayncondcdDaoDAO.im_zsc_ints_payn_cond_cd_do0001(listInts);
                } else if (("2").equals(listInts.getStatus())) {
                    
                    resultInts = comCgAmImSecuritiesinqrpritmgmtImzscintspayncondcdDaoDAO.im_zsc_ints_payn_cond_cd_so0003(listInts);
                    if (resultInts.getCnt() > 0) {
                        errCd = "E00000";
                        errMsg = "동일한 조건이 있습니다.";
                        throw new CgAppUserException("CG_ERROR", 0, CodeUtil.getCodeValue("CGMsgCode", "E", errCd, new String[] { errMsg }), errCd);
                    }
                    comCgAmImSecuritiesinqrpritmgmtImzscintspayncondcdDaoDAO.im_zsc_ints_payn_cond_cd_io0001(listInts);
                } else if (("1").equals(listInts.getStatus())) {
                    
                    comCgAmImSecuritiesinqrpritmgmtImzscintspayncondcdDaoDAO.im_zsc_ints_payn_cond_cd_uo0001(listInts);
                }
            }
            
            vldtDcntCondCdDoc = /* 주석처리(as-is) XMLUtil.toXML(XMLUtil.getVector(pDoc, "VLDT_DCNT_COND_CD_LIST"))*/;
            ArrayList aryListVldt = /* 수동가이드 예정 (as-is) XMLUtil.toArrayList(vldtDcntCondCdDoc)*/;
            Iterator<SecuritiesInqrPritMgmtVo> itrVldt = aryListVldt.iterator();
            while (itrVldt.hasNext()) {
                listVldt = itrVldt.next();
                
                listVldt.setLastChnrId((String) UserHeaderUtil.getInstance().getEmpno());
                
                listVldt.setLastChngDttm((String) UserHeaderUtil.getInstance().getTimestamp());
                
                if (("3").equals(listVldt.getStatus())) {
                    
                    resultVldt = comCgAmImSecuritiesinqrpritmgmtImzscstrcvldtdcntcondDaoDAO.im_zsc_strc_vldt_dcnt_cond_so0001(listVldt);
                    if (resultVldt.getCnt() > 0) {
                        errCd = "E00000";
                        errMsg = "현재 사용하고 있는 조건입니다.";
                        throw new CgAppUserException("CG_ERROR", 0, CodeUtil.getCodeValue("CGMsgCode", "E", errCd, new String[] { errMsg }), errCd);
                    }
                    comCgAmImSecuritiesinqrpritmgmtImzscvldtdcntcondcdDaoDAO.im_zsc_vldt_dcnt_cond_cd_do0001(listVldt);
                } else if (("2").equals(listVldt.getStatus())) {
                    
                    resultVldt = comCgAmImSecuritiesinqrpritmgmtImzscvldtdcntcondcdDaoDAO.im_zsc_vldt_dcnt_cond_cd_so0003(listVldt);
                    if (resultVldt.getCnt() > 0) {
                        errCd = "E00000";
                        errMsg = "동일한 조건이 있습니다.";
                        throw new CgAppUserException("CG_ERROR", 0, CodeUtil.getCodeValue("CGMsgCode", "E", errCd, new String[] { errMsg }), errCd);
                    }
                    comCgAmImSecuritiesinqrpritmgmtImzscvldtdcntcondcdDaoDAO.im_zsc_vldt_dcnt_cond_cd_io0001(listVldt);
                } else if (("1").equals(listVldt.getStatus())) {
                    
                    comCgAmImSecuritiesinqrpritmgmtImzscvldtdcntcondcdDaoDAO.im_zsc_vldt_dcnt_cond_cd_uo0001(listVldt);
                }
            }
        } catch (ElException e) {
            throw new CgAppUserException("CG_ERROR", 0, e.getMessage(), "SPLT0003", e);
        }
        
        return result;
    }

}